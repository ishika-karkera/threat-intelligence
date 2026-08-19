import feedparser
from datetime import datetime, timedelta, timezone
from dateutil import parser as dateparser

RSS_SOURCES = {
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "Krebs on Security": "https://krebsonsecurity.com/feed/",
}

def fetch_rss(url, source_name):
    feed = feedparser.parse(url)
    return [{"title": e.title, "link": e.link, "summary": e.get("summary",""),
              "published": e.get("published",""), "source": source_name}
             for e in feed.entries]

def filter_recent(articles, days=3):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    recent = []
    for a in articles:
        try:
            pub = dateparser.parse(a["published"])
            if pub.tzinfo is None:
                pub = pub.replace(tzinfo=timezone.utc)
            if pub >= cutoff:
                recent.append(a)
        except Exception:
            continue
    return recent

def fetch_all_sources():
    all_articles = []
    for name, url in RSS_SOURCES.items():
        try:
            recent = filter_recent(fetch_rss(url, name))
            all_articles.extend(recent)
            print(f"{name}: {len(recent)} recent articles")
        except Exception as e:
            print(f"Failed {name}: {e}")
    return all_articles

if __name__ == "__main__":
    for a in fetch_all_sources():
        print(f"[{a['source']}] {a['title']}")
