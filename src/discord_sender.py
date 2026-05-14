import json
import requests

_CATEGORY_META = {
    'general':  {'label': '🎮 게임 개발', 'color': 0x1E3A8A},
    'economy':  {'label': '📊 게임 경제', 'color': 0x14532D},
    'world_it': {'label': '🌐 세계 IT',   'color': 0x4C1D95},
}


class DiscordSender:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_news(self, news_items: list, category: str = 'general'):
        if not news_items:
            return

        meta = _CATEGORY_META.get(category, _CATEGORY_META['general'])

        # 헤더 메시지
        requests.post(self.webhook_url, json={
            'content': f"**오늘의 {meta['label']} 뉴스** ({len(news_items)}건)"
        }, timeout=10)

        # 기사별 embed — 제목 + 요약을 복사하기 좋게 분리
        for item in news_items:
            summary = item.get('summary_text', '요약 없음')
            embed = {
                'color': meta['color'],
                'fields': [
                    {
                        'name': '📌 제목',
                        'value': f"[{item.title}]({item.link})",
                        'inline': False,
                    },
                    {
                        'name': '📝 요약',
                        'value': summary,
                        'inline': False,
                    },
                ],
                'footer': {'text': item.get('source', '')},
            }
            resp = requests.post(
                self.webhook_url,
                json={'embeds': [embed]},
                timeout=10,
            )
            if resp.status_code not in (200, 204):
                print(f"[discord] 전송 실패: {resp.status_code} {resp.text[:200]}")
