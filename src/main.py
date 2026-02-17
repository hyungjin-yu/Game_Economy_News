import schedule
import time
import os
import sys

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config_manager import ConfigManager
from src.news_scraper import NewsScraper
from src.summarizer import Summarizer
from src.discord_sender import DiscordSender

import logging

# Configure logging
logging.basicConfig(
    filename='activity.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def job():
    logging.info("Starting scheduled job...")
    print("Starting scheduled job...")
    try:
        config_manager = ConfigManager()
        
        rss_urls = config_manager.get("rss_feeds", [])
        scraper = NewsScraper(rss_urls)
        news_items = scraper.fetch_latest_news(10)
        
        if not news_items:
            logging.info("No news items found.")
            return

        api_key = config_manager.get("openai_api_key")
        # Handle placeholder
        if api_key == "YOUR_OPENAI_API_KEY_HERE":
            api_key = None
            
        summarizer = Summarizer(api_key)
        
        # Process summaries
        logging.info(f"Summarizing {len(news_items)} articles...")
        for item in news_items:
            # feedparser usually puts content in 'summary' or 'description'
            content = item.get('summary', '') or item.get('description', '')
            item['summary_text'] = summarizer.summarize(content, item.title)
        
        webhook_url = config_manager.get("discord_webhook_url")
        if webhook_url and webhook_url != "YOUR_WEBHOOK_URL_HERE":
            sender = DiscordSender(webhook_url)
            sender.send_news(news_items)
            logging.info("News sent to Discord successfully.")
            print("News sent to Discord successfully.")
        else:
            logging.warning("Discord Webhook URL not configured.")
            
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

def main():
    # If standard run, just log startup
    if len(sys.argv) > 1 and sys.argv[1] == "--run-now":
        job()
        return

    print("Game Dev News Notifier started in Loop Mode.")
    logging.info("Game Dev News Notifier started in Loop Mode.")
    
    # Load config to get schedule time
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
