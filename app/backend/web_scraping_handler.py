from init import db
from summary_handler import Summarizer
from db_handler import DatabaseHandler
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import time

class Scraper:
    def __init__(self):
        self.summarizer = Summarizer()
        self.db_handler = DatabaseHandler()
    
    def fetch_book_metadata(self,base_url, book_id):
        """
        Fetch metadata for a specific book by its ID.

        Args:
            base_url (str): The base URL of Project Gutenberg.
            book_id (str): The ID of the book.

        Returns:
            dict: Metadata for the book, including title, author, language, etc.
        """
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

            return {
                "title": title,
                "author": author,
                "language": language,
                "subject": subjects,
                "image_url": image_url,
                "amazon_url": self.scrape_amazon(title),
                "summary": self.summarizer.generate_summary(text_url)
            }
        except Exception as e:
            print(f"Failed to fetch metadata for book ID {book_id}: {e}")
            return None
        
    def scrape_amazon(self,title):
        """
        Search Amazon for a book title and return the most relevant product link.

        Args:
            title (str): The book title to search for.

        Returns:
            str: The URL of the most relevant product, or None if no match is found.
        """
        try:
            search_url = f"https://www.amazon.com/s?k={requests.utils.quote(title)}"
            
            HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

            webpage = requests.get(search_url, headers=HEADERS)
            soup = BeautifulSoup(webpage.content, "html.parser")
            
            products = soup.find_all("div",attrs={"data-component-type":"s-search-result"})
            best_match = None
            best_score = 0

            for product in products[:10]: 
                title_element = product.find("h2", attrs={'class':'a-size-medium a-spacing-none a-color-base a-text-normal'})

                link_element = product.find('a', {'class': 'a-link-normal s-line-clamp-2 s-link-style a-text-normal'})
    
                if title_element and link_element:
                    product_title = title_element.get_text(strip=True)
        
                    product_link = f"https://www.amazon.com{link_element['href']}"
        
                    score = fuzz.partial_ratio(title.lower(), product_title.lower())
                    if score > best_score:
                        best_score = score
                        best_match = product_link

            return best_match

        except Exception as e:
            print(f"Failed to fetch Amazon link for {title}: {e}")
            return None


    def scrape_gutenberg(self):
        base_url = "https://www.gutenberg.org"
        books_page = f"{base_url}/browse/scores/top"

        response = requests.get(books_page)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        book_links = soup.select('ol li a[href^="/ebooks/"]')

        books = []

        batch_size = 3
        start = 8
        limit = 50

        for i in range(start, limit, batch_size):

            batch = book_links[i:i + batch_size]

            for book_link in batch:
                book_id = book_link["href"].split("/")[-1]
                metadata = self.fetch_book_metadata(base_url, book_id)
                if metadata:
                    books.append(metadata)
            
            if i + batch_size < len(books):
                print(f"Waiting for {60} seconds before processing the next batch...")
                time.sleep(60)

        self.db_handler.add_books(books)
        

