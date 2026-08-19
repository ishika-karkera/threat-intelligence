from fetch import fetch_all_sources
from extract import extract_ttp_ids

articles = fetch_all_sources()

for article in articles:
    ttps = extract_ttp_ids(article["title"] + " " + article["summary"])
    if ttps:  # only print articles where something was actually found
        print("Article:", article["title"])
        print("Extracted TTPs:", ttps)
        print("---")
