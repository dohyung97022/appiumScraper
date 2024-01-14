from src import setup
from src.twitter.service import twitter_scraper_automation_service
from src.youtube.service import youtube_service

if __name__ == '__main__':
    setup.configure()
    twitter_scraper_automation_service.loop_scrape_posts(50)
    twitter_scraper_automation_service.loop_scrape_users(50)
    youtube_service.loop_scrape_videos('', 'Shorts', 50)
