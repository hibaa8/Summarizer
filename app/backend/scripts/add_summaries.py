from backend.services.gutenberg_web_scraper import GutenbergScraper
from ..app import create_app

app = create_app()

# navigate to the app dir and run python3 -m backend.scripts.add_summaries to add additional books
if __name__ == '__main__':
    with app.app_context():
        scrapper = GutenbergScraper()
        scrapper.scrape_gutenberg(100)