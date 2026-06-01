from datetime import datetime
import sys
import os
from dotenv import load_dotenv
from crawler import WebsiteCrawler
from page_finder import PageFinder
from extractor import DataExtractor
from llm_extractor import LLMExtractor
from schemas import (
    UniversityData,
    Overview,
    Contact,
    AdmissionDeadline,
    TuitionItem,
    PageMetadata,
    Location
)
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
def main():
    domain = sys.argv[1]
    crawler = WebsiteCrawler(max_depth=2)
    urls = crawler.crawl(domain)
    finder = PageFinder()
    admissions_page = finder.find_admissions_page(urls)
    tuition_page = finder.find_tuition_page(urls)
    extractor = DataExtractor()
    homepage_html = extractor.fetch_page(domain)
    university_name = extractor.extract_university_name(homepage_html)
    admissions_html = extractor.fetch_page(admissions_page)
    admissions_text = extractor.extract_text(admissions_html)
    tuition_html = extractor.fetch_page(tuition_page)
    tuition_text = extractor.extract_text(tuition_html)
    tuition_cost = extractor.extract_tuition(tuition_text)
    email = extractor.extract_email(admissions_text)
    phone = extractor.extract_phone(admissions_text)
    deadline = extractor.extract_deadline(admissions_text)
    llm_data = {}
    if api_key:
        try:
            combined_text = homepage_html
            llm = LLMExtractor(api_key)
            llm_data = llm.extract_structured_data(
                combined_text
            )
            logging.info("Using LLM fallback")
        except Exception as e:
            print(f"LLM fallback failed: {e}")
            llm_data = {}
    location = Location(
        city=llm_data.get("city"),
        state=llm_data.get("state"),
        country=llm_data.get("country")
    )
    tuition_value = None
    if tuition_cost:
        tuition_value = int(
            tuition_cost.replace("$", "")
            .replace(",", "")
        )
    elif llm_data.get("tuition"):
        tuition_value = llm_data.get("tuition")
    final_deadline = deadline or llm_data.get("deadline")
    result = UniversityData(
        overview=Overview(
            university_name=university_name,
            location=location,
            contact=Contact(
                email=email,
                phone=phone
            )
        ),
        admission_deadlines=[
            AdmissionDeadline(
                deadline_date=final_deadline
            )
        ],
        tuition_breakdown=[
            TuitionItem(
                fee_type="Tuition",
                cost=tuition_value,
                currency="USD"
            )
        ],
        page_metadata=[
            PageMetadata(
                url=admissions_page,
                page_title=extractor.extract_page_title(
                    admissions_html
                ),
                scraped_at=datetime.now().isoformat(),
                status_code="200"
            ),
            PageMetadata(
                url=tuition_page,
                page_title=extractor.extract_page_title(
                    tuition_html
                ),
                scraped_at=datetime.now().isoformat(),
                status_code="200"
            )
        ]
    )
    logging.info("Execution Summary")
    logging.info(f"URLs Crawled: {len(urls)}")
    logging.info(f"Admissions Page: {admissions_page}")
    logging.info(f"Tuition Page: {tuition_page}")
    logging.info(f"University: {university_name}")
    print(result.model_dump_json(indent=4))
if __name__ == "__main__":
    main()