"""
indexer.py
Author: Alex Matei
This script is responsible for crawling web pages, processing the HTML files to 
extract text, and creating an inverted index of stemmed tokens and their
frequencies. The inverted index is then saved to a file.

To use this script:
1. Set the seed URLs, allowed domains, crawl ID, and other parameters in the 
    global constants section.
2. Call the `crawl()` function to start crawling the web pages.
3. Call the `process_repository()` function to process the crawled HTML files
    and create the inverted index.
4. The inverted index will be serialized and saved by pickle to a file named
    "inverted_index.pkl".

To load the inverted index later, you can use:
pickle.load(open("inverted_index.pkl", "rb"))
"""

from webcrawler import WebCrawler
from tokenizer import clean_HTML, tokenize, stem
from nltk.corpus import stopwords
from collections import Counter
import pickle
import os

# Global Constants
STOP_WORDS = stop_words = set(stopwords.words("english"))
SEED_URLS = ["https://en.wikipedia.org/wiki/Everything", "https://en.wikipedia.org/wiki/Pride_and_Prejudice", "https://en.wikipedia.org/wiki/Caviar", "https://en.wikipedia.org/wiki/Iran", "https://en.wikipedia.org/wiki/Barbie", "https://en.wikipedia.org/wiki/Taoism", "https://en.wikipedia.org/wiki/Mariah_Carey", "https://en.wikipedia.org/wiki/Saurischia"]
LANGUAGE = "en"
ALLOWED_DOMAINS = [f"{LANGUAGE}.wikipedia.org"]
CRAWL_ID = "wikipedia_crawl_without_hashing"
MAX_PAGES = 500

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
    """
    inverted_index = {}  # dictionary to store the inverted index
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
                continue #skips processing/indexing if the document fails
            for term, freq in stemmed_frequencies.items():
                if term not in inverted_index:
                    inverted_index[term] = Counter()  # Initialize a Counter for each term
                inverted_index[term][filename] = freq  # Add the frequency for the current document
    return inverted_index

def main():
    try:
        crawl()  # Uncomment to crawl
        inverted_index = process_repository(f"repository_{CRAWL_ID}")  # Process the repository
        pickle.dump(inverted_index, open("inverted_index_2.pkl", "wb"))  # Save the inverted index to a file
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

