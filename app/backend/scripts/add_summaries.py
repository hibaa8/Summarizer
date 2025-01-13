from backend.services.gutenberg_web_scraper import GutenbergScraper
from ..app import create_app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        scrapper = GutenbergScraper()
        scrapper.scrape_gutenberg(100)