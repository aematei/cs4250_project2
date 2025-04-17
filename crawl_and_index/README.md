# How to Use `indexer.py`

This script crawls web pages, processes their HTML content, and creates an inverted index of stemmed tokens and their frequencies. Additionally, it tracks inlinks and outlink counts using a `LinkTracker` DataFrame. Both the inverted index and the link tracker are saved as pickle files (`inverted_index.pkl` and `link_tracker.pkl`) for further use.

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
     - Save the link tracker to [link_tracker.pkl](https://github.com/aematei/cs4250_project2/tree/main/crawl_and_index/indexer.py).

3. **Load the Inverted Index and Link Tracker:**
   - To use the inverted index in another script:
     ```python
     import pickle
     inverted_index = pickle.load(open("inverted_index_3.pkl", "rb"))
     ```
   - To use the link tracker in another script:
     ```python
     import pickle
     link_tracker = pickle.load(open("link_tracker.pkl", "rb"))
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
     - Tracks inlinks and outlink counts for each page using the `LinkTracker` class.

3. **Output:**
   - The inverted index is a dictionary:
     ```python
     {
         "word1": Counter({"doc1.html": 3, "doc2.html": 5}),
         "word2": Counter({"doc3.html": 2}),
         ...
     }
     ```
   - The link tracker is a DataFrame:
     ```
     url             | inlinks       | outlink_count | page_rank
     -----------------------------------------------------------
     "page1.html"    | {"page2"}     | 1             | None
     ```
   - These structures allow efficient word lookups, frequency analysis, and link analysis.

### The writeup for my part of the report

Crawling and Indexing - Alex + Team:
To create the index, I used our crawler and tokenizer/stemmer from our last submission. I also added stop word removal as part of the tokenizer/stemmer pipeline, so that we could avoid common words that wouldn’t help in the long run.

Our team crawled 500 pages restricted to the en.wikipedia.org domain, with a set of diverse seed URL's to diversify our digital corpus. Once I had the page URLs, I programmatically generated a Python collections.Counter object (i.e. a wrapper class that enhances the dictionary data structure) which I learned about when developing on this project. This conveniently counted the instances of each unique, stemmed token. 

To create the inverse index with counts, I used a dictionary with nested Counter objects that tracked the documents associated with each term, as well as the frequency of each term in that document. The structure was essentially {term: {document_id: frequency}, …}. In order to store the index as a file, I utilized pickle to serialize the nested dictionary structure. This allowed our team to “unpickle” the index file back into the original Python object form, preserving the efficiency of the nested dictionary structure.

Additionally, I needed to create a new data structure to track outlinks for each page. This was implemented using a `LinkTracker` class, which stores inlinks and outlink counts in a DataFrame. While the actual outlinks are not stored in the serialized DataFrame, this structure will still be critical for PageRank calculations down the line, as it allows us to analyze the link relationships between pages efficiently. The `LinkTracker` was also serialized using pickle for easy reuse in future analyses.
