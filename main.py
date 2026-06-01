from datetime import datetime
from crawler import WebsiteCrawler
from page_finder import PageFinder
from extractor import DataExtractor
from schemas import (
    UniversityData,
    Overview,
    Contact,
    AdmissionDeadline,
    TuitionItem,
    PageMetadata
)
def main():
    domain = "https://www.bucknell.edu"
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
    result = UniversityData(
    overview=Overview(
        university_name=university_name,
        contact=Contact(
            email=email,
            phone=phone)),
    admission_deadlines=[
        AdmissionDeadline(
            deadline_date=deadline)],
    tuition_breakdown=[
        TuitionItem(
            fee_type="Tuition",cost=int(tuition_cost.replace("$", "").replace(",", "")) if tuition_cost else None,currency="USD")],
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
    print(result.model_dump_json(indent=4))
if __name__ == "__main__":
    main()