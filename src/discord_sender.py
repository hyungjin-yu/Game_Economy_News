import requests
import json

class DiscordSender:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_news(self, news_items):
        if not news_items:
            return

        embeds = []
        for item in news_items:
            summary = item.get('summary_text', '요약 없음')
            embed = {
                "title": item.title,
                "url": item.link,
                "description": summary,
                "footer": {
                    "text": f"Source: {item.get('source', 'Unknown')}"
                },
                "color": 5814783 # Discord Blue-ish
            }
            embeds.append(embed)

        # Discord webhooks have limits (10 embeds per message).
        # Split if necessary.
        chunk_size = 10
        for i in range(0, len(embeds), chunk_size):
            chunk = embeds[i:i + chunk_size]
            data = {
                "content": f"📢 **오늘의 게임 개발 뉴스** ({len(news_items)}건)",
                "embeds": chunk
            }
            response = requests.post(self.webhook_url, json=data)
            if response.status_code != 204:
                print(f"Failed to send to Discord: {response.status_code}, {response.text}")
