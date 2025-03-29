from webcrawler import WebCrawler

if __name__ == "__main__":
    seed_urls = ["https://en.wikipedia.org/wiki/Everything"]
    allowed_domains = ["wikipedia.org"]
    crawl_id = "crawl_1"
    max_pages = 500
    language = "en"

    web_crawler = WebCrawler(seed_urls, allowed_domains, crawl_id, max_pages, language)
    web_crawler.crawl()
