from .amazon_web_scraper import AmazonScraper
from backend.database.db_handler import DatabaseHandler
from .llm_summary_generator import LLMSummaryGenerator
import requests
from bs4 import BeautifulSoup
import time
import requests
import re

class GutenbergScraper:
    def __init__(self):
        self.amazon_scraper = AmazonScraper()
        self.db_handler = DatabaseHandler()
        self.llm_agent = LLMSummaryGenerator()

    def _fetch_full_text(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            full_text = response.text

            start = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK", full_text, re.IGNORECASE)
            end = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK", full_text, re.IGNORECASE)
            return full_text[start.end():end.start()].strip() if start and end else None
            
        except Exception as e:
            print(f"Error fetching full text from {url}: {e}")
            return None
    
    def _fetch_book_metadata(self,base_url, book_id):
        book_url = f"{base_url}/ebooks/{book_id}"
        response = requests.get(book_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        try:
            title_tag = soup.find("td", {"itemprop":"headline"})
            if title_tag:
                title = title_tag.text.strip()
            else:
                title = "Unknown Title"

            author_tag = soup.find("a", {"itemprop":"creator"})
            if author_tag:
                author = ",".join(author_tag.text.strip().split(',')[:2])
            else:
                author = "Unknown Author"

            language_tag = soup.find("tr", {"property": "dcterms:language"})
            if language_tag:
                language = language_tag.find("td").text.strip()
            else:
                language = "Unknown Language"

            subject_tags = soup.find_all("a", href=lambda href: href and href.startswith("/ebooks/subject"))
            subjects = ", ".join(tag.text.strip() for tag in subject_tags) if subject_tags else "Unknown Category"

            image_tag = soup.find("meta", {"property": "og:image"})
            image_url = image_tag["content"] if image_tag else "Unknown Image"

            text_link = soup.find("a", href=True, text="Plain Text UTF-8")
            text_url = f"{base_url}{text_link['href']}" if text_link else None

            full_text = self._fetch_full_text(text_url)
            if full_text:
                summary = self.llm_agent.call_llm(full_text)
            else:
                summary = ""

            return {
                "title": title,
                "author": author,
                "language": language,
                "subject": subjects,
                "image_url": image_url,
                "amazon_url": self.amazon_scraper.scrape_amazon(title),
                "summary": summary
            }
        except Exception as e:
            print(f"Failed to fetch metadata for book ID {book_id}: {e}")
            return None


    def scrape_gutenberg(self, end):
        base_url = "https://www.gutenberg.org"
        books_page = f"{base_url}/browse/scores/top"
        response = requests.get(books_page)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        book_links = soup.select('ol li a[href^="/ebooks/"]')

        batch_size = 1
        start = 101
        end += start

        for i in range(start, end, batch_size):
            batch = book_links[i:i + batch_size]
            for book_link in batch:
                book_id = book_link["href"].split("/")[-1]
                metadata = self._fetch_book_metadata(base_url, book_id)
                if metadata:
                    self.db_handler.add_book(metadata)
            
            if i + batch_size < end:
                print(f"Waiting for {60} seconds before processing the next batch...")
                time.sleep(60)

        

