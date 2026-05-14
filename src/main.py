import json
import logging
import os
import requests
import schedule
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config_manager import ConfigManager
from src.news_scraper import NewsScraper
from src.summarizer import Summarizer
from src.discord_sender import DiscordSender

logging.basicConfig(
    filename='activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SEEN_URLS_FILE = os.path.join(_PROJECT_ROOT, 'data', 'seen_urls.json')
_MAX_SEEN = 200


def _load_seen_urls() -> set:
    if not os.path.exists(_SEEN_URLS_FILE):
        return set()
    with open(_SEEN_URLS_FILE, 'r', encoding='utf-8') as f:
        return set(json.load(f).get('urls', []))


def _save_seen_urls(seen: set):
    os.makedirs(os.path.dirname(_SEEN_URLS_FILE), exist_ok=True)
    urls = list(seen)[-_MAX_SEEN:]
    with open(_SEEN_URLS_FILE, 'w', encoding='utf-8') as f:
        json.dump({'urls': urls}, f, ensure_ascii=False, indent=2)


def _notify_error(webhook_url: str, error: Exception):
    if not webhook_url or "YOUR_" in webhook_url:
        return
    try:
        requests.post(webhook_url, json={
            "content": f"⚠️ **Game Economy News 봇 오류**\n```{str(error)[:1000]}```"
        }, timeout=5)
    except Exception:
        pass


def job():
    logging.info("Starting scheduled job...")
    print("Starting scheduled job...")

    config_manager = ConfigManager()
    general_webhook = config_manager.get("discord_webhook_url", "")

    try:
        feeds_config = config_manager.get("feeds")
        if not feeds_config:
            logging.info("Using legacy rss_feeds config.")
            feeds_config = {"general": config_manager.get("rss_feeds", [])}

        openai_key = config_manager.get("openai_api_key")
        if openai_key == "YOUR_OPENAI_API_KEY_HERE":
            openai_key = None

        gemini_key = config_manager.get("gemini_api_key")
        if gemini_key == "YOUR_GEMINI_API_KEY_HERE":
            gemini_key = None

        summarizer = Summarizer(openai_api_key=openai_key, gemini_api_key=gemini_key)
        seen_urls = _load_seen_urls()

        for category, urls in feeds_config.items():
            if not urls:
                continue

            logging.info(f"Processing category: {category}")

            if category == "economy":
                webhook_url = config_manager.get("discord_economy_webhook_url")
            else:
                webhook_url = general_webhook

            if not webhook_url or "YOUR_" in webhook_url:
                logging.warning(f"Webhook URL for {category} not configured. Skipping.")
                continue

            scraper = NewsScraper(urls)
            all_items = scraper.fetch_latest_news(10)

            # 중복 제거
            new_items = [item for item in all_items if item.link not in seen_urls]
            if not new_items:
                logging.info(f"No new articles for {category} (all already sent).")
                continue

            new_items = new_items[:5]
            logging.info(f"Summarizing {len(new_items)} new articles for {category}...")

            for item in new_items:
                # 기사 본문 우선, 없으면 RSS 요약으로 폴백
                body = scraper.fetch_article_content(item.link)
                content = body or item.get('summary', '') or item.get('description', '')
                item['summary_text'] = summarizer.summarize(content, item.title)

            sender = DiscordSender(webhook_url)
            sender.send_news(new_items)
            logging.info(f"{category.capitalize()} news sent to Discord successfully.")

            for item in new_items:
                seen_urls.add(item.link)

        _save_seen_urls(seen_urls)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        _notify_error(general_webhook, e)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--run-now":
        job()
        return

    print("Game Dev News Notifier started in Loop Mode.")
    logging.info("Game Dev News Notifier started in Loop Mode.")

    try:
        config_manager = ConfigManager()
        scheduled_time = config_manager.get("scheduled_time", "09:50")
    except Exception:
        scheduled_time = "09:50"

    print(f"Scheduled to run at {scheduled_time} daily.")
    schedule.every().day.at(scheduled_time).do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
