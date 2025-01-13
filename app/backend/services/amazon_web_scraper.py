# from init import db
import requests
from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz

class AmazonScraper:

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