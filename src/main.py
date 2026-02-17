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
        
        # Determine feeds structure
        feeds_config = config_manager.get("feeds")
        if not feeds_config:
            # Legacy support
            logging.info("Using legacy rss_feeds config.")
            feeds_config = {
                "general": config_manager.get("rss_feeds", [])
            }

        # API Keys setup
        openai_key = config_manager.get("openai_api_key")
        if openai_key == "YOUR_OPENAI_API_KEY_HERE": openai_key = None
            
        gemini_key = config_manager.get("gemini_api_key")
        if gemini_key == "YOUR_GEMINI_API_KEY_HERE": gemini_key = None
            
        summarizer = Summarizer(openai_api_key=openai_key, gemini_api_key=gemini_key)

        # Process each category
        for category, urls in feeds_config.items():
            if not urls:
                continue
                
            logging.info(f"Processing category: {category}")
            
            # Determine Webhook URL based on category
            if category == "economy":
                webhook_url = config_manager.get("discord_economy_webhook_url")
            else:
                webhook_url = config_manager.get("discord_webhook_url")

            if not webhook_url or "YOUR_" in webhook_url:
                logging.warning(f"Webhook URL for {category} not configured. Skipping.")
                continue

            # Scrape
            scraper = NewsScraper(urls)
            news_items = scraper.fetch_latest_news(5) # Fetch top 5 per category
            
            if not news_items:
                logging.info(f"No news items found for {category}.")
                continue

            # Summarize
            logging.info(f"Summarizing {len(news_items)} articles for {category}...")
            for item in news_items:
                content = item.get('summary', '') or item.get('description', '')
                item['summary_text'] = summarizer.summarize(content, item.title)
            
            # Send
            sender = DiscordSender(webhook_url)
            # Add category prefix to title for clarity? Optional.
            sender.send_news(news_items)
            logging.info(f"{category.capitalize()} news sent to Discord successfully.")

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
