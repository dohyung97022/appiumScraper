from src import setup
from src.twitter.service import twitter_scraper_automation_service

if __name__ == '__main__':
    setup.configure()
    twitter_scraper_automation_service.loop_scrape_users(100)
