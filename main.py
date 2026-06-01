from crawler import WebsiteCrawler

def main():
    domain = "https://www.bucknell.edu"
    crawler = WebsiteCrawler(max_depth=2)
    urls = crawler.crawl(domain)
    print(f"\nFound {len(urls)} URLs\n")
    for url in urls[:20]:
        print(url)

if __name__ == "__main__":
    main()