import feedparser
import requests
import time
from bs4 import BeautifulSoup

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


class NewsScraper:
    def __init__(self, rss_urls):
        self.rss_urls = rss_urls

    def fetch_latest_news(self, limit=10):
        all_entries = []
        for url in self.rss_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                entry['source'] = feed.feed.title if 'title' in feed.feed else url
                all_entries.append(entry)

        all_entries.sort(key=lambda x: x.get('published_parsed', time.localtime(0)), reverse=True)
        return all_entries[:limit]

    def fetch_article_content(self, url: str, max_chars: int = 3000) -> str:
        """기사 URL에서 본문 텍스트 추출. 실패 시 빈 문자열 반환."""
        try:
            response = requests.get(url, headers=_HEADERS, timeout=8)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")

            for tag in soup(["script", "style", "nav", "footer", "aside", "header"]):
                tag.decompose()

            container = soup.find("article") or soup.find("main") or soup.body
            if not container:
                return ""

            paragraphs = container.find_all("p")
            text = " ".join(
                p.get_text(strip=True)
                for p in paragraphs
                if len(p.get_text(strip=True)) > 30
            )
            return text[:max_chars]
        except Exception:
            return ""


if __name__ == "__main__":
    scraper = NewsScraper(["https://www.gamedeveloper.com/rss.xml"])
    news = scraper.fetch_latest_news(5)
    for n in news:
        print(f"- {n.title} ({n.link})")
