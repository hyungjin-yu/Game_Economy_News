import json
import requests


class DiscordSender:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_header(self, category: str, count: int):
        labels = {'general': '🎮 게임 개발', 'economy': '📊 게임 경제', 'world_it': '🌐 세계 IT'}
        label = labels.get(category, category)
        data = {"content": f"**오늘의 {label} 뉴스** ({count}건)"}
        requests.post(self.webhook_url, json=data, timeout=10)

    def send_card(self, item: dict, image_path: str):
        """기사 1건을 이미지 카드 + 링크로 전송"""
        content = f"**{item.title}**\n{item.link}"
        with open(image_path, 'rb') as f:
            resp = requests.post(
                self.webhook_url,
                files={'file': ('card.png', f, 'image/png')},
                data={'payload_json': json.dumps({'content': content})},
                timeout=30,
            )
        if resp.status_code not in (200, 204):
            print(f"[discord] 전송 실패: {resp.status_code} {resp.text[:200]}")

    def send_news(self, news_items: list):
        """레거시: embed 방식 전송"""
        if not news_items:
            return
        embeds = []
        for item in news_items:
            embeds.append({
                "title": item.title,
                "url": item.link,
                "description": item.get('summary_text', '요약 없음'),
                "footer": {"text": f"Source: {item.get('source', 'Unknown')}"},
                "color": 5814783,
            })
        for i in range(0, len(embeds), 10):
            data = {
                "content": f"📢 오늘의 뉴스 ({len(news_items)}건)",
                "embeds": embeds[i:i + 10],
            }
            resp = requests.post(self.webhook_url, json=data, timeout=10)
            if resp.status_code not in (200, 204):
                print(f"[discord] 전송 실패: {resp.status_code}")
