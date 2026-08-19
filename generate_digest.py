import json, os, hashlib
from fetch import fetch_all_sources
from extract import extract_ttp_ids
from dql_templates import DQL_TEMPLATES

def article_id(a):
    return hashlib.md5(a["link"].encode()).hexdigest()

def load_seen():
    if os.path.exists("seen_articles.json"):
        with open("seen_articles.json") as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    with open("seen_articles.json", "w") as f:
        json.dump(list(seen), f)

def build_incident(article):
    ttp_ids = extract_ttp_ids(article["title"] + " " + article["summary"])
    ttps = []
    for tid in ttp_ids:
        entry = DQL_TEMPLATES.get(tid)
        ttps.append({"id": tid, "name": entry["name"] if entry else "Unknown",
                      "status": "covered" if entry else "gap",
                      "query": entry["query"] if entry else ""})
    return {"source": article["source"], "title": article["title"],
            "summary": article["summary"][:200], "ttps": ttps}

def main():
    os.makedirs("docs", exist_ok=True)
    seen = load_seen()
    articles = fetch_all_sources()
    new_articles = [a for a in articles if article_id(a) not in seen]

    incidents = [build_incident(a) for a in new_articles]

    digest_path = "docs/digest.json"
    existing = {"incidents": []}
    if os.path.exists(digest_path):
        with open(digest_path) as f:
            existing = json.load(f)

    all_incidents = (incidents + existing.get("incidents", []))[:30]
    all_ttps = [t for inc in all_incidents for t in inc["ttps"]]

    stats = {
        "attacks_tracked": len(all_incidents),
        "ttps_identified": len(all_ttps),
        "queries_ready": len([t for t in all_ttps if t["status"] == "covered"]),
        "coverage_gaps": len([t for t in all_ttps if t["status"] == "gap"]),
    }

    with open(digest_path, "w") as f:
        json.dump({"stats": stats, "incidents": all_incidents}, f, indent=2)

    for a in new_articles:
        seen.add(article_id(a))
    save_seen(seen)
    print(f"Done. {len(new_articles)} new articles processed.")

if __name__ == "__main__":
    main()
