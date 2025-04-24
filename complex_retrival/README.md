# How to Use `bm25_retrival.py` 

This script implements the BM25 simple search system. It takes a user query and returns relevant documents in ranked order. The index (`index_3.pkl`) and inverted_index (`inverted_index_3.plk`) are "unpickled", and manipulated to create a web_page ranking.

## Prerequisites: 
- **Python 3** This script requires Python 3 to run
- **External Libraries**:
  - `pickle` for loading the pre-built index and inverted index.
  - `nltk` (Natural Language Toolkit) for text processing.

## Steps to Use:
1. **Prepare your Environment**
   - Ensure you have the following:
     - An index (`index_3.pkl`) and inverted_index (`inverted_index_3.plk`)
     - A Corpus of documents stored in (`repository_wikipedia_crawl_with_link_tracker/`)

2. **Run the Script**
    -Change directories into (`complex_retrival`)
    -Execute the script:
        ```bash
        python3 bm25_retrival.py
        ```
    -This calculates the average document length for the corpus.
    -Then, it prompts the user for a query, processing the query to remove stopwords and stem 
    -The BM25 score is calculated for every document given the query terms
    -Finally, it displays a rank of relevant documents. 

## How It Works:
1. **User Query:**
   - The user types in their search query in the terminal.
   - The query is split into individual terms and processed by:
     - *Stemming*: Using the Porter Stemmer to reduce words to their base form (e.g., "running" becomes "run").
     - *Stopword Removal*: Filtering out common words like "the", "and", "in", etc., to improve search relevance.

2. **BM25 Scores Calculated**
    -The Binary Independence Score is Calculated
        -pi -> the number of relevant documents in the corpus
        -si -> the number of non-relevant documents that contain a query term in all non-relevant documents
    -The Document Weight is Calculated
        -fi -> the frequency of a query term in a given document
        -k1, K -> empirically set values
    -The Query Weight is Calculated
        -qfi -> the frequency of the query term
        -k2 -> empirically set value
    -The values are multiplied together, and the scores are added for all query terms to form the final BM25 score

3. **Output**
    -The documents are ranked by their relevance score and displayed as a string:
        ```python
        "The top results are: . . ."
        ```
    -The documents are listed by their title and relevance score
