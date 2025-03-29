# How to Use `indexer.py`

This script crawls web pages, processes their HTML content, and creates an inverted index of stemmed tokens and their frequencies. The inverted index is saved as a pickle file (`inverted_index.pkl`) for further use.

## Steps to Use:
1. **Set Parameters:**
   - Update the global constants:
     - `SEED_URLS`: List of starting URLs for crawling.
     - `ALLOWED_DOMAINS`: Domains to restrict crawling.
     - `CRAWL_ID`: Unique identifier for the crawl (used for directory naming).
     - `MAX_PAGES`: Maximum number of pages to crawl.
     - `LANGUAGE`: Language filter for crawled pages (e.g., `"en"` for English).

2. **Run the Script:**
   - Execute the script:
     ```bash
     python indexer.py
     ```
   - This will:
     - Crawl the web starting from [SEED_URLS](https://github.com/aematei/cs4250_project2/tree/main/crawl_and_index/indexer.py).
     - Save crawled HTML files in a directory named `repository_<CRAWL_ID>`.
     - Process the HTML files to create an inverted index.
     - Save the inverted index to [inverted_index.pkl](https://github.com/aematei/cs4250_project2/tree/main/crawl_and_index/indexer.py).

3. **Load the Inverted Index:**
   - To use the inverted index in another script:
     ```python
     import pickle
     inverted_index = pickle.load(open("inverted_index.pkl", "rb"))
     ```

## How It Works:
1. **Crawling:**
   - The [crawl()](https://github.com/aematei/cs4250_project2/tree/main/crawl_and_index/webcrawler.py) function uses the [WebCrawler](https://github.com/aematei/cs4250_project2/tree/main/crawl_and_index/webcrawler.py) class to fetch web pages, save their HTML content, and generate a report of out-links.

2. **Processing:**
   - The [process_repository()](https://github.com/aematei/cs4250_project2/tree/main/crawl_and_index/indexer.py) function processes each HTML file:
     - Extracts text using [clean_HTML](https://github.com/aematei/cs4250_project2/tree/main/crawl_and_index/tokenizer.py).
     - Tokenizes and stems the text.
     - Removes stop words.
     - Builds an inverted index where each word maps to a [Counter](https://github.com/aematei/cs4250_project2/tree/main/crawl_and_index/indexer.py) of document frequencies.

3. **Output:**
   - The inverted index is a dictionary:
     ```python
     {
         "word1": Counter({"doc1.html": 3, "doc2.html": 5}),
         "word2": Counter({"doc3.html": 2}),
         ...
     }
     ```
   - This structure allows efficient word lookups and frequency analysis.
