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

### The writeup for my part of the report

Crawling and Indexing - Alex
To create the index, I used our crawler and tokenizer/stemmer from our last submission. I ran into an issue with language detection, since some non-english languages were slipping through. I had to make minor adjustments to the webcrawler to fix this. I also added stop word removal as part of the tokenizer/stemmer pipeline, so that we could avoid common words that wouldn’t help in the long run.

I crawled 500 pages restricted to the wikipedia.org domain, with the seed URL being https://en.wikipedia.org/wiki/Everything. This seed had no problem giving us plenty of outlinks. Once I had the page URLs, I went through each one and generated a Python collections.Counter object, which is essentially a wrapper class that enhances the dictionary data structure (I didn’t know about this before researching for this project). This conveniently counted the instances of each unique, stemmed token. To create the inverse index with counts, I simply created a dictionary with nested Counter objects that tracked the documents associated with each term, as well as the frequency of each term in that document. The structure was essentially {term: {document_id: frequency}, …}. In order to store the index as I file, I decided to use the Python pickle library to serialize the nested dictionary structure. This allowed my team members to “unpickle” the index file back into the original Python object form, preserving the efficiency of the nested dictionary structure.  
