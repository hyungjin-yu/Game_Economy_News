import feedparser
from datetime import datetime
import time

class NewsScraper:
    def __init__(self, rss_urls):
        self.rss_urls = rss_urls

    def fetch_latest_news(self, limit=10):
        all_entries = []
        for url in self.rss_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # Add source for context
                entry['source'] = feed.feed.title if 'title' in feed.feed else url
                all_entries.append(entry)
        
        # Sort by published date (descending)
        # Handle different date formats or missing dates if necessary
        # Usually feedparser normalizes this to 'published_parsed'
        all_entries.sort(key=lambda x: x.get('published_parsed', time.localtime(0)), reverse=True)
        
        return all_entries[:limit]

if __name__ == "__main__":
    # Test
    scraper = NewsScraper(["https://www.gamedeveloper.com/rss.xml"])
    news = scraper.fetch_latest_news(5)
    for n in news:
        print(f"- {n.title} ({n.link})")
