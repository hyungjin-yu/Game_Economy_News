import json
import logging
import os
import requests
import schedule
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config_manager import ConfigManager
from src.discord_sender import DiscordSender
from src.news_scraper import NewsScraper
from src.summarizer import Summarizer

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
    with open(_SEEN_URLS_FILE, 'w', encoding='utf-8') as f:
        json.dump({'urls': list(seen)[-_MAX_SEEN:]}, f, ensure_ascii=False, indent=2)


def _notify_error(webhook_url: str, error: Exception):
    if not webhook_url or 'YOUR_' in webhook_url:
        return
    try:
        requests.post(
            webhook_url,
            json={'content': f'⚠️ **Game Economy News 봇 오류**\n```{str(error)[:1000]}```'},
            timeout=5,
        )
    except Exception:
        pass


def _get_webhook(config: ConfigManager, category: str) -> str:
    mapping = {
        'economy':  'discord_economy_webhook_url',
        'world_it': 'discord_world_it_webhook_url',
    }
    return config.get(mapping.get(category, 'discord_webhook_url'), '')


def job():
    logging.info("Starting scheduled job...")
    print("Starting scheduled job...")

    config = ConfigManager()
    general_webhook = config.get('discord_webhook_url', '')

    try:
        feeds_config = config.get('feeds')
        if not feeds_config:
            feeds_config = {'general': config.get('rss_feeds', [])}

        openai_key = config.get('openai_api_key')
        if openai_key == 'YOUR_OPENAI_API_KEY_HERE':
            openai_key = None
        gemini_key = config.get('gemini_api_key')
        if gemini_key == 'YOUR_GEMINI_API_KEY_HERE':
            gemini_key = None

        summarizer = Summarizer(openai_api_key=openai_key, gemini_api_key=gemini_key)
        seen_urls = _load_seen_urls()

        for category, urls in feeds_config.items():
            if not urls:
                continue

            webhook_url = _get_webhook(config, category)
            if not webhook_url or 'YOUR_' in webhook_url:
                logging.warning(f"Webhook for '{category}' not configured. Skipping.")
                continue

            logging.info(f"Processing category: {category}")

            scraper = NewsScraper(urls)
            all_items = scraper.fetch_latest_news(15)
            new_items = [item for item in all_items if item.link not in seen_urls][:5]

            if not new_items:
                logging.info(f"No new articles for '{category}'.")
                continue

            logging.info(f"{len(new_items)} new articles for '{category}'.")

            for item in new_items:
                body = scraper.fetch_article_content(item.link)
                content = body or item.get('summary', '') or item.get('description', '')
                item['summary_text'] = summarizer.summarize(content, item.title)
                seen_urls.add(item.link)

            sender = DiscordSender(webhook_url)
            sender.send_news(new_items, category)
            logging.info(f"'{category}' done.")

        _save_seen_urls(seen_urls)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        _notify_error(general_webhook, e)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--run-now':
        job()
        return

    print("Game Dev News Notifier started.")
    logging.info("Game Dev News Notifier started.")

    try:
        scheduled_time = ConfigManager().get('scheduled_time', '09:50')
    except Exception:
        scheduled_time = '09:50'

    print(f"Scheduled to run at {scheduled_time} daily.")
    schedule.every().day.at(scheduled_time).do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
