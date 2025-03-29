import csv
import os
import langid
import requests
from queue import Queue
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


def download_page(url):
    """Download and save the HTML content of the page.
    :arg url: The URL to download
    :returns text of html response string
    """
    try:
        response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return None


def detect_language(text):
    """Using the langid library, it returns the language of a string sequence \n
    :argument text: the text to identify \n
    :returns language of given input
    """
    if text is None or text == "":
        return None

    return langid.classify(text)[0]


class WebCrawler:
    def __init__(self, seed_urls, allowed_domains, crawl_id, max_pages=50, language="en"):
        self.seed_urls = seed_urls
        self.allowed_domains = allowed_domains
        self.max_pages = max_pages
        self.visited_urls = set()
        self.to_crawl = Queue()
        self.language = language
        self.repository_path = f"repository_{crawl_id}"
        self.report_file = f"report_{crawl_id}.csv"
        # make unique directory for each input
        os.makedirs(self.repository_path, exist_ok=True)

    def is_valid_domain(self, url):
        """Check if the URL is within the allowed domain(s).
        :arg url: The URL to check.
        :return: True if the URL is within the allowed domain(s)."""
        parsed_url = urlparse(url)
        return any(domain in parsed_url.netloc for domain in self.allowed_domains)

    def save_page(self, url, content):
        """Save the HTML page to the repository.
        :argument url: The URL to save.
        :argument content: The HTML content to save."""
        filename = os.path.join(self.repository_path, f"{hash(url)}.html")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

    def extract_links(self, html, base_url):
        """Extract and return all valid outlinks from a page.
        :argument html: The HTML page to extract links from.
        :argument base_url: The URL to extract links from.
        :returns links extracted."""
        soup = BeautifulSoup(html, "html.parser")
        links = set()
        for link in soup.find_all("a", href=True):
            absolute_url = urljoin(base_url, link["href"])
            if self.is_valid_domain(absolute_url):
                links.add(absolute_url)
        return links

    def crawl(self):
        """Crawl web pages starting from the seed URLs."""
        for url in self.seed_urls:
            self.to_crawl.put(url)

        with open(self.report_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["URL", "Out-links"])

            while not self.to_crawl.empty() and len(self.visited_urls) < self.max_pages:
                url = self.to_crawl.get()
                if url in self.visited_urls:
                    continue

                print(f"Crawling: {url}")
                html_content = download_page(url)
                if not html_content: #if html_content is None
                    continue

                #print(detect_language(html_content))
                if detect_language(html_content) != self.language:
                    continue

                self.visited_urls.add(url)
                self.save_page(url, html_content)
                out_links = self.extract_links(html_content, url)

                #write url to report.csv
                writer.writerow([url, len(out_links)])
                
                for link in out_links:
                    if link not in self.visited_urls:
                        self.to_crawl.put(link)