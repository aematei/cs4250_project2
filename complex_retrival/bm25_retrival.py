import math
import os
import pickle
from nltk.stem import *
from nltk.corpus import stopwords
from collections import Counter

def get_document_list():
    inverted_index = pickle.load(open("../crawl_and_index/inverted_index_3.pkl", "rb"))  # open the index
    unique_webpage = set()
    for key, value in inverted_index.items():
        for web_page in value:
            unique_webpage.add(web_page)
    return unique_webpage

def get_document_count(dir_path = ""):
    """Returns the number of documents in the collection based on the directory path given
    :param dir_path: Path to the documents collection"""
    if dir_path == "":
        unique_webpage = get_document_list()
        return len(unique_webpage)

    else:
        for root, directory, web_pages in os.walk(dir_path): #traverse a directory
            return len(web_pages)
        else:
            return 0 #if the walk is unsuccessful, return 0

def get_average_document_length(dir_path = ""):
    """Returns the average document length of the collection
    :param dir_path: Path to the documents collection"""
    try: #due to the time complexity of calculation, value is saved into file
        with open("average_document_length.txt", "r") as file:
            average = float(file.readline())
    except FileNotFoundError:
        if dir_path == "": #assumes we aren't given a directory path name
            inverted_index = pickle.load(open("../crawl_and_index/inverted_index_3.pkl", "rb"))
            unique_webpages = set()
            document_length = list()
            for key, value in inverted_index.items():
                for web_page in value:
                    unique_webpages.add(web_page)
            for web_page in unique_webpages:
                document_length.append(get_document_length(web_page, index=True))

        else:
            document_length = list()
            for root, directory, web_pages in os.walk(dir_path): #traverse a directory
                for web_page in web_pages: #for each webpage in the directory
                    file_name = f"../crawl_and_index/repository_wikipedia_crawl_with_link_tracker/{web_page}"
                    document_length.append(get_document_length(file_name))

        try:
            average = sum(document_length) // len(document_length)
        except ZeroDivisionError:#len(doc_len) can be 0 which would lead to an average of 0
            average = 0

        with open("average_document_length.txt", "w") as file: #save number to text file for later retrival
            file.write(str(average))
    return average


def get_document_length(file_path, index=True):
    """Returns the average document length of the collection
    :param file_path: Path to the file
    :param index: If True, uses index to retrieve document length"""
    if not index:
        try:
            with open(file_path, 'r', errors="ignore") as file:
                length = len(file.read().split())
        except FileNotFoundError:
            print (f"File {file_path} not found, length assumed to be 0")
            length = 0
        return length

    elif index:
        de_inverted_index = pickle.load(open("../crawl_and_index/index_3.pkl", "rb"))
        word_counter = de_inverted_index[file_path]
        word_list = [word for word in word_counter.elements()]
        return len(word_list)


class BinaryIndependence:
    @staticmethod
    def find_relevant_doc_count():
        """Returns the number of relevant documents to a term"""
        return 0

    @staticmethod
    def find_total_of_relevant_doc():
        """Returns the total number of relevant documents"""
        return 0

    @staticmethod
    def find_non_relevant_doc_count(term):
        """Returns the number of documents that a term occurs in"""
        inverted_index = pickle.load(open("../crawl_and_index/inverted_index_3.pkl", "rb"))
        return len(inverted_index[term].keys())

    def find_binary_independence_value(self, term):

        r_i = self.find_relevant_doc_count()
        R = self.find_total_of_relevant_doc()

        n_i = self.find_non_relevant_doc_count(term)
        N = get_document_count()

        p_i = (r_i + 0.5) / (R + 1)
        s_i = (n_i - r_i + 0.5) / (N - R + 1)

        return math.log2(p_i / s_i)

class DocWeights:

    @staticmethod
    def find_term_frequency(term, file_name):
        inverted_index = pickle.load(open("../crawl_and_index/inverted_index_3.pkl", "rb"))
        for web_page, word_count in inverted_index[term].items():
            if web_page == file_name:
                return word_count

        return 0

    @staticmethod
    def find_K_value(file_name, k_i=1.2, b=0.75):
        doc_length = get_document_length(file_name, index=True)
        ave_doc_length = get_average_document_length(file_name)

        return k_i * (doc_length / ave_doc_length + (b + (1-b)))

    def find_doc_weight(self, term, file_name):
        k_1 = 1.2 #emperical value based on TREC value
        f_i = self.find_term_frequency(term, file_name)
        K = self.find_K_value(file_name)

        return (f_i * (k_1 + 1)) / (K + f_i)

class QueryTermWeights:
    @staticmethod
    def find_query_term_frequency(query_list, query_term):
        frequency = 0
        for terms in query_list:
            if query_term == terms:
                frequency += 1
        return frequency

    def find_query_term_weight(self, query_list, query_term ):

        k_2 = 500 #emperical value based on TRED value between 0:1000
        qf_i = self.find_query_term_frequency(query_list, query_term)

        return (qf_i * (k_2 + 1)) / (k_2 + qf_i)

def calculate_BM25(query_list, query_term, document_rank):
    unique_webpages = get_document_list()
    binary_independence = BinaryIndependence()
    doc_weights = DocWeights()
    query_term_weights = QueryTermWeights()

    #calculate binary independence value
    b_i_value = binary_independence.find_binary_independence_value(query_term)
    print("Binary independence value: ", b_i_value)

    #calculate query term weight value
    q_t_w_value = query_term_weights.find_query_term_weight(query_list, query_term)
    print("Query term weight: ", q_t_w_value)

    for web_page in unique_webpages:
        d_w_value = doc_weights.find_doc_weight(query_term, web_page)
        print(f"{query_term} | {web_page}:    Document weight: ", d_w_value)


        BM25_score = b_i_value * d_w_value * q_t_w_value
        try:
            document_rank[web_page] += BM25_score
        except KeyError:
            document_rank[web_page] = BM25_score

    return document_rank

def welcome_screen():
    print("""Hello and Welcome to the BM25 Search Engine! 
    Some background processes are occurring, but you should soon be able to 
    query to your hearts content""")

def generator_list(list):
    for entry in list:
        yield f"'{entry[0]}': Score '{entry[1]}'"

def main():
    import time
    welcome_screen()
    get_average_document_length() #by doing this process early on, we can save repeated computational use later on

    # initialize porter stemmer and stop words
    porter_stem = PorterStemmer()
    stop_words = set(stopwords.words('english'))

    query_input = input("Hello! Input your query here... ").lower().split()
    query_terms_stemmed = [porter_stem.stem(term) for term in query_input]
    # resource used: https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
    query_terms_stopped = [term for term in query_terms_stemmed if not term.lower() in stop_words]

    start_time = time.time()
    document_rank = dict()
    for term in query_terms_stopped:
        document_rank = calculate_BM25(query_list=query_terms_stopped, query_term = term, document_rank=document_rank)

    document_rank = sorted(document_rank.items(), key=lambda x: x[1], reverse=True) #sort the documents by BM25 score
    end_time = start_time - time.time()
    results_generator = generator_list(document_rank)

    print(f"{end_time}The top results are:")
    while True:
        for i in range(10):
            print (next(results_generator))

        more_results = bool(input("Do you want more results? Type 'yes' or leave blank"))
        if not more_results:
            break

if __name__ == '__main__':
    main()