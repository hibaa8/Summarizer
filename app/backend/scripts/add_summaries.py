from backend.services.gutenberg_web_scraper import GutenbergScraper
from ..app import create_app

app = create_app()

# script to add more books to database.
# can be run from the app dir after correct setup (see requirements.txt). Run: python3 -m backend.scripts.add_summaries.
if __name__ == '__main__':
    with app.app_context():
        scrapper = GutenbergScraper()
        scrapper.scrape_gutenberg(100)