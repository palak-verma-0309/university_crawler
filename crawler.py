from collections import deque
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

class WebsiteCrawler:
    def __init__(self, max_depth=2):
        self.max_depth = max_depth

    def get_links(self, url):
        links = set()
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup.find_all("a", href=True):
                links.add(tag["href"])

        except Exception as e:
            print(f"Error crawling {url}: {e}")

        return links

    def crawl(self, start_url):
        visited = set()
        discovered_urls = set()
        domain = urlparse(start_url).netloc
        queue = deque([(start_url, 0)])
        while queue:
            current_url, depth = queue.popleft()
            if current_url in visited:
                continue
            visited.add(current_url)
            discovered_urls.add(current_url)
            if depth >= self.max_depth:
                continue

            links = self.get_links(current_url)

            for link in links:
                absolute_url = urljoin(current_url, link)
                if absolute_url.lower().endswith(".pdf"):
                    continue
                parsed = urlparse(absolute_url)

                if parsed.netloc != domain:
                    continue

                if absolute_url not in visited:
                    queue.append((absolute_url, depth + 1))
        return list(discovered_urls)