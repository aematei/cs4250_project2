import csv
import string
import os
from langid import classify  # Import langid for language detection
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

def is_a_duplicate(text):
    """Checks for duplicate urls within wikipedia"""
    url_duplicates = ["#cite_note", "#cite_ref", "#CITEREF", "Special", "#", "wlittle=", "%", "index.php", "File:", "Tanjung_Malim", "Gabriela_Duarte"]

    for url_duplicate in url_duplicates:
        if text.find(url_duplicate) != -1:
            return True
        else:
            continue

    return False

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

    def save_page(self, url, content, hashed = False):
        """Save the HTML page to the repository.
        :argument url: The URL to save.
        :argument content: The HTML content to save."""
        if hashed:
            filename = os.path.join(self.repository_path, f"{hash(url)}.html")
        else:
            page_name = url.replace("https:", "").replace(".html", "").replace("//en.wikipedia.org/","").replace("wiki/", "")
            for char in ['/', ':', '*', '?', '<', '>', '\"', "|"]: #prevent error no 22
                page_name = page_name.replace(char, "")
            filename = os.path.join(self.repository_path, f"{page_name[:63]}.html")

        with open(filename, "w", encoding="utf-8") as file:
            file.write(content)

    def extract_links(self, html, base_url):
        """Extract and return all valid out-links from a page.
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

            doc_count = 1  # Initialize document count

            while not self.to_crawl.empty():
                if len(self.visited_urls) >= self.max_pages:
                    break #break if we've reached over our count for pages

                url = self.to_crawl.get()
                if url in self.visited_urls:
                    continue

                if is_a_duplicate(url):
                    continue

                print(f"[{doc_count}] Crawling: {url}")  # Add doc count to status message
                html_content = download_page(url)
                if not html_content:  # if html_content is None
                    continue

                # Detect language using langid
                if classify(html_content)[0] != self.language:
                    print(f"Skipping URL {url} due to language mismatch")
                    continue  # Skip this page if the language doesn't match

                self.visited_urls.add(url)
                self.save_page(url, html_content)
                out_links = self.extract_links(html_content, url)

                doc_count += 1  # Increment document count only for successfully visited pages

                # write url to report.csv
                writer.writerow([url, len(out_links)])

                for link in out_links:
                    if link not in self.visited_urls:
                        self.to_crawl.put(link)