# import necessary libraries
import pickle
import nltk
import os
from bs4 import BeautifulSoup
from nltk.stem import *
from nltk.corpus import stopwords
# download NLTK's stopwords list
nltk.download('stopwords')

def intersection(array1, array2):
    """Finds the intersection of two arrays"""
    results = set(array1).intersection(set(array2))
    return list(results)

def find_relevant_docs(index, query_terms):
    """Finds the relevant documents for a given query and index"""
    relevant_docs = {}
    # iterates through query terms
    for query in query_terms:
        # if query term is in index, add it to relevant_docs
        if query in index:
            relevant_docs[query] = list(index[query].keys())
        else:
            # if no docs found for query terms, return false
            print("No docs relevant to this query.")
            return False
    #print(relevant_docs)
    return relevant_docs # returns dictionary of relevant docs

def find_docs_with_all_queries(relevant_docs):
    """Finds documents that contain all query terms"""
    docs = None
    # iterate through relevant docs for each query term
    for term in relevant_docs:
        if docs == None:
            # initialize with first query term's docs
            docs = relevant_docs[term]
        else:
            # update docs to include those with current term(s)
            docs = intersection(docs, relevant_docs[term])
            #print(docs)
    return docs # returns docs with all query terms

def show_relevant_docs(docs):
    """displays titles of relevant documents"""
    # resource used: https://www.geeksforgeeks.org/python-read-file-from-sibling-directory/
    
    path = os.path.realpath(__file__) # get current file path
    current_dir = os.path.dirname(path) # get current directory path
    dir = os.path.dirname(path) # get parent directory path
    dir = dir.replace("simple_retrieval", "crawl_and_index") # modify path to directory with docs
    os.chdir(dir) # change directory to the one with the html docs
    #print(os.getcwd())

    result = "" # stores titles of relevant documents
    # iterate over docs and get their titles
    for doc in docs:
        # open doc and use BeautifulSoup to get its ttle
        soup = BeautifulSoup(open(f"repository_wikipedia_crawl/{doc}"), "html.parser")
        # append doc's title to result string
        result += f"\"{soup.title.string}\", "
    os.chdir(current_dir) # change back to original directory
    #print(os.getcwd())
    print(f"Relevant results are: {result[:-2]}") # print titles of relevant docs

def main():
    """main function to handle query and search process"""
    # load inverted index
    inverted_index = pickle.load(open("inverted_index.pkl", "rb"))
    #print(inverted_index)

    # initialize stemmer and stop words
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))

    # get user query, splite into terms, then process it
    query = input("Enter your query search here: ")
    query_terms = query.split()
    #print(query_terms)
    query_terms = [stemmer.stem(term) for term in query_terms]
    #print(query_terms)
    # resource used: https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
    query_terms = [term for term in query_terms if not term.lower() in stop_words]
    #print(query_terms)

    # find relevant docs for query terms
    relevant_docs = find_relevant_docs(inverted_index, query_terms)

    # if relevant docs found, find docs with all query terms
    if relevant_docs:
        docs_all_terms = find_docs_with_all_queries(relevant_docs)
        # print(ind)
        # print(docs_all_terms)
        show_relevant_docs(docs_all_terms)    
    else:
        print("Please type a different query.")

main() # call main function
