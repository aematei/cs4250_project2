# How to Use `simple_retrieval.py`

This script implements a simple search system using a boolean retrieval system (logical AND is performed). It takes a user's query, processes it, and returns relevant documents from a pre-built inverted index. The inverted index is loaded from a pickle file (`inverted_index.pkl`), and the results are displayed by extracting titles from HTML documents stored locally.

## Prerequisites:
- **Python 3**: This script requires Python 3 to run.
- **External Libraries**: 
  - `nltk` (Natural Language Toolkit) for text processing.
  - `BeautifulSoup` from `bs4` for parsing HTML documents.
  - `pickle` for loading the pre-built inverted index.

## Steps to Use:
1. **Prepare the Environment:**
   - Ensure you have the following:
     - A pre-built **inverted index** saved as `inverted_index.pkl`.
     - HTML files representing documents stored in a folder named `repository_wikipedia_crawl/`.

2. **Run the Script:**
   - Change directories into `simple_retrieval`.
   - Execute the script:
     ```bash
     python3 simple_retrieval.py
     ```
   - This will:
     - Prompt the user the enter their query in the terminal.
     - Split and process the query terms, removing common stopwords and stemming the remaining terms.
     - Search the inverted index for any documents containing all the terms in the query.
     - Display the relevant documents (if any exist containing all the query terms).

## How It Works:
1. **User Query:**
   - The user types in their search query in the terminal.
   - The query is split into individual terms and processed by:
     - *Stemming*: Using the Porter Stemmer to reduce words to their base form (e.g., "running" becomes "run").
     - *Stopword Removal*: Filtering out common words like "the", "and", "in", etc., to improve search relevance.

2. **Boolean Retrieval System:**
   - The program uses a boolean retrieval system to check if all the query terms can be found in the index.
     - If any term is missing from the index, the search will return no results.
     - If all terms are found, the program checks which documents contain all of the terms.
   - If the terms are located, the program finds the documents associated with each term and checks which documents contain all terms in the query.

3. **Output:**
   - The relevant documents are displayed as a string:
     ```python
     "Relevant results are: . . . "
     ```
   - The documents are listed using the title of the web page returned.