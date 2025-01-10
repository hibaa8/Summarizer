from web_scraping_handler import Scraper
from init import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        scrapper = Scraper()
        scrapper.scrape_gutenberg()