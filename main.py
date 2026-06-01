from crawler import WebsiteCrawler
from page_finder import PageFinder
def main():
    domain = "https://www.bucknell.edu"
    crawler = WebsiteCrawler(max_depth=2)
    urls = crawler.crawl(domain)

    finder = PageFinder()

    admissions_page = finder.find_admissions_page(
        urls
    )

    tuition_page = finder.find_tuition_page(
        urls
    )

    print("\nAdmissions Page:")
    print(admissions_page)

    print("\nTuition Page:")
    print(tuition_page)

if __name__ == "__main__":
    main()