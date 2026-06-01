from crawler import WebsiteCrawler
from page_finder import PageFinder
from extractor import DataExtractor
from schemas import (
    UniversityData,
    Overview,
    Contact,
    AdmissionDeadline,
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
    email = extractor.extract_email(admissions_text)
    phone = extractor.extract_phone(admissions_text)
    deadline = extractor.extract_deadline(admissions_text)
    result = UniversityData(
        overview=Overview(university_name=university_name,contact=Contact(email=email,phone=phone)),
        admission_deadlines=[AdmissionDeadline(deadline_date=deadline)])
    print(result.model_dump_json(indent=4))
if __name__ == "__main__":
    main()