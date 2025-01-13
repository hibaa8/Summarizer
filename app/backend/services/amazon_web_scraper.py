import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

class AmazonScraper:
    def __init__(self):
        self.base_url = "https://www.amazon.com/s?k="
        self.headers = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

    def scrape_amazon(self, title):
        try:
            search_url = self._build_search_url(title)
            soup = self._fetch_search_results(search_url)
            return self._find_best_match(soup, title)
        except Exception as e:
            print(f"Failed to fetch Amazon link for {title}: {e}")
            return None

    def _build_search_url(self, title):
        return f"{self.base_url}{requests.utils.quote(title)}"

    def _fetch_search_results(self, url):
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")

    def _find_best_match(self, soup, title):
        products = soup.find_all("div", attrs={"data-component-type": "s-search-result"})
        best_match = None
        best_score = 0

        for product in products[:10]:
            title_element = product.find("h2", attrs={'class': 'a-size-medium a-spacing-none a-color-base a-text-normal'})
            link_element = product.find('a', {'class': 'a-link-normal s-line-clamp-2 s-link-style a-text-normal'})

            if title_element and link_element:
                product_title = title_element.get_text(strip=True)
                product_link = f"https://www.amazon.com{link_element['href']}"
                score = fuzz.partial_ratio(title.lower(), product_title.lower())

                if score > best_score:
                    best_score = score
                    best_match = product_link

        return best_match
