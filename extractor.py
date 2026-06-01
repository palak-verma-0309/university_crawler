import re
import requests
from bs4 import BeautifulSoup

class DataExtractor:

    def fetch_page(self, url):
        try:
            response = requests.get(
                url,
                timeout=10
            )
            response.raise_for_status()
            return response.text

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""

    def extract_text(self, html):
        soup = BeautifulSoup(html,"html.parser")
        return soup.get_text(separator=" ",strip=True)

    def extract_email(self, text):
        emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",text)
        return emails[0] if emails else None

    def extract_phone(self, text):
        phones = re.findall(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
        return phones[0] if phones else None
    
    def extract_deadline(self, text):
        pattern = (
            r"(January|February|March|April|May|June|July|August|September|October|November|December)"
            r"\s+\d{1,2}"
        )
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )
        if match:
            return match.group(0)
        return None