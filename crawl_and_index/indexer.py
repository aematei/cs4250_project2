"""
indexer.py
Author: Alex Matei
This script is responsible for crawling web pages, processing the HTML files to 
extract text, and creating an inverted index of stemmed tokens and their
frequencies. It also tracks inlinks, outlinks, and outlink counts using a
LinkTracker DataFrame.
"""

from webcrawler import WebCrawler
from tokenizer import clean_HTML, tokenize, stem
from nltk.corpus import stopwords
from collections import Counter
from link_tracker import LinkTracker  # Import the LinkTracker module
import pickle
import os

# Global Constants
STOP_WORDS = stop_words = set(stopwords.words("english"))
SEED_URLS = ["https://en.wikipedia.org/wiki/Everything", "https://en.wikipedia.org/wiki/Pride_and_Prejudice", "https://en.wikipedia.org/wiki/Caviar", "https://en.wikipedia.org/wiki/Iran", "https://en.wikipedia.org/wiki/Barbie", "https://en.wikipedia.org/wiki/Taoism", "https://en.wikipedia.org/wiki/Mariah_Carey", "https://en.wikipedia.org/wiki/Saurischia"]
LANGUAGE = "en"
ALLOWED_DOMAINS = [f"{LANGUAGE}.wikipedia.org"]
CRAWL_ID = "wikipedia_crawl_with_link_tracker"
MAX_PAGES = 10
INVERTED_INDEX_FILENAME = "inverted_index_3.pkl"


def crawl():
    """
    Hardcoded function to crawl web pages and save the HTML files.
    Output: a repository of HTML files and a report file.
    """
    web_crawler = WebCrawler(SEED_URLS, ALLOWED_DOMAINS, CRAWL_ID, MAX_PAGES, LANGUAGE)
    web_crawler.crawl()


def process_document(doc_path):
    """
    This function processes text in the HTML file and returns the stemmed tokens and their frequencies.
    Output: a Counter() instance with stemmed tokens and their frequencies. This can be treated as a dictionary.
    """
    text = clean_HTML(doc_path)  # extracts text from HTML
    tokens = tokenize(text)  # tokenizes text
    stopped = [term for term in tokens if term not in STOP_WORDS]  # removes stop words
    try:
        stemmed_tokens = stem(stopped)  # stems tokens; can change how to stem tokens based on language of text
        stemmed_frequencies = Counter(stemmed_tokens)  # counts stemmed tokens
        return stemmed_frequencies
    except Exception as e:
        print(f"Error processing document {doc_path}: {e}")


def process_repository(directory):
    """
    This function applies text processing to the HTML files in a given directory.
    It also updates the LinkTracker with inlinks and outlinks.
    """
    inverted_index = {}  # dictionary to store the inverted index
    link_tracker = LinkTracker()  # Initialize the LinkTracker
    web_crawler = WebCrawler(SEED_URLS, ALLOWED_DOMAINS, CRAWL_ID, MAX_PAGES, LANGUAGE)  # Create an instance
    page_count = 0  # counter for the number of pages read

    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            page_count += 1  # increment the page count
            file_path = os.path.join(directory, filename)
            print(f"[{page_count}] Processing {file_path}")  # print the page count and file being processed
            try:
                stemmed_frequencies = process_document(file_path)  # process the document
            except AttributeError as e:
                print(f"Error processing document {file_path}: {e}")
                continue  # skips processing/indexing if the document fails

            # Update the inverted index
            for term, freq in stemmed_frequencies.items():
                if term not in inverted_index:
                    inverted_index[term] = Counter()  # Initialize a Counter for each term
                inverted_index[term][filename] = freq  # Add the frequency for the current document

            # Extract outlinks from the document and update the LinkTracker
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
            outlinks = web_crawler.extract_links(html_content, filename)  # Use the instance
            link_tracker.add_page(filename, outlinks)

    # Save the LinkTracker DataFrame to a pickle file
    link_tracker.save_to_pickle(f"link_tracker_{CRAWL_ID}.pkl")

    return inverted_index


def main():
    try:
        crawl()  # Uncomment to crawl
        inverted_index = process_repository(f"repository_{CRAWL_ID}")  # Process the repository
        pickle.dump(inverted_index, open(f"{INVERTED_INDEX_FILENAME}", "wb"))  # Save the inverted index to a file
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

