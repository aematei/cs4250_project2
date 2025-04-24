import math
import os
import pickle
from nltk.stem import *
from nltk.corpus import stopwords

def get_document_list(inverted_index=None):
    if inverted_index is None:
        inverted_index = pickle.load(open("../crawl_and_index/inverted_index_3.pkl", "rb"))  # open the index
        print ("get_document_list pickle")
    unique_webpage = set()
    for key, value in inverted_index.items():
        for web_page in value:
            unique_webpage.add(web_page)
    return unique_webpage

def get_document_count(inverted_index=None):
    """Returns the number of documents in the collection based on the directory path given"""
    unique_webpage = get_document_list(inverted_index)
    return len(unique_webpage)

def pre_compute_document_length(inverted_index=None):
    if os.path.exists('bm25_retrival.pkl'):
        return None
    else:
        if inverted_index is None:
            inverted_index = pickle.load(open("../crawl_and_index/inverted_index_3.pkl", "rb"))
            #print("pre_compute_doc_length pickle")
        unique_webpages = set()
        document_length = dict()
        for key, value in inverted_index.items():
            for web_page in value:
                unique_webpages.add(web_page)
        for web_page in unique_webpages:
            document_length[web_page] = get_document_length(web_page)

        pickle.dump(document_length, open(f"bm25_document_lengths.pkl", "wb")) #save the document lengths in a file


def get_average_document_length():
    """Returns the average document length of the collection"""
    try: #due to the time complexity of calculation, value is saved into file
        with open("average_document_length.txt", "r") as file:
            average = float(file.readline())
    except FileNotFoundError:
        inverted_index = pickle.load(open("../crawl_and_index/inverted_index_3.pkl", "rb"))
        unique_webpages = set()
        document_length = list()
        for key, value in inverted_index.items():
            for web_page in value:
                unique_webpages.add(web_page)
        for web_page in unique_webpages:
            document_length.append(get_document_length(web_page))

        try:
            average = sum(document_length) // len(document_length)
        except ZeroDivisionError:#len(doc_len) can be 0 which would lead to an average of 0
            average = 0

        with open("average_document_length.txt", "w") as file: #save number to text file for later retrival
            file.write(str(average))
    return average


def get_document_length(file_path, document_lengths=None):
    """Returns the average document length of the collection
    :param file_path: Path to the file
    :param document_lengths: If not None, uses document_length to retrieve document length"""

    try:
        if document_lengths is None:
            document_lengths = pickle.load(open("bm25_document_lengths.pkl", "rb"))
        return document_lengths[file_path]
    except FileNotFoundError:
        de_inverted_index = pickle.load(open("../crawl_and_index/index_3.pkl", "rb"))
        word_counter = de_inverted_index[file_path]
        word_list = [word for word in word_counter.elements()]
        return len(word_list)

class BinaryIndependence:
    def __init__ (self, inverted_index):
        self.inverted_index = inverted_index

    @staticmethod
    def find_relevant_doc_count():
        """Returns the number of relevant documents to a term"""
        return 0

    @staticmethod
    def find_total_of_relevant_doc():
        """Returns the total number of relevant documents"""
        return 0

    def find_non_relevant_doc_count(self, term):
        """Returns the number of documents that a term occurs in
        :param term: the query term searched for"""
        try:
            return len(self.inverted_index[term].keys())
        except KeyError:
            return 0

    def find_binary_independence_value(self, term):

        r_i = self.find_relevant_doc_count()
        R = self.find_total_of_relevant_doc()

        n_i = self.find_non_relevant_doc_count(term)
        N = get_document_count(self.inverted_index)

        p_i = (r_i + 0.5) / (R + 1)
        s_i = (n_i - r_i + 0.5) / (N - R + 1)

        return math.log2(p_i / s_i)

class DocWeights:
    def __init__(self, inverted_index, document_lengths):
        self.inverted_index = inverted_index
        self.document_lengths = document_lengths

    def find_term_frequency(self, term, file_name):
        """The frequency of a term in a document
        :param term: term to search for
        :param file_name: name of the file"""
        try:
            for web_page, word_count in self.inverted_index[term].items():
                if web_page == file_name:
                    return word_count
        except KeyError: #the word doesn't exist in the inverted index
            return 0

        return 0

    def find_K_value(self, file_name, k_i=1.2, b=0.75):
        """An empirically set value based on the document length and average document length
        :param file_name: Path to the file
        :param k_i: empirically set value
        :param b: empirically set value"""
        doc_length = get_document_length(file_name, document_lengths=self.document_lengths)
        ave_doc_length = get_average_document_length()

        return k_i * (doc_length / ave_doc_length + (b + (1-b)))

    def find_doc_weight(self, term, file_name):
        """Calculate the weights for each given document
        :param term: term to search for
        :param file_name: name of the file to search through"""
        k_1 = 1.2 #emperical value based on TREC value
        f_i = self.find_term_frequency(term, file_name)
        K = self.find_K_value(file_name)

        return (f_i * (k_1 + 1)) / (K + f_i)

class QueryTermWeights:
    @staticmethod
    def find_query_term_frequency(query_list, query_term):
        """Calculates the frequency (i.e. how often it appears) of a query term
        :param query_list: List of query terms
        :param query_term: a term from the query"""
        frequency = 0
        for terms in query_list:
            if query_term == terms:
                frequency += 1
        return frequency

    def find_query_term_weight(self, query_list, query_term ):
        """Calculates the weight given to the query term
        :param query_list: List of query terms
        :param query_term: a term from the query"""

        k_2 = 500 #emperical value based on TRED value between 0:1000
        qf_i = self.find_query_term_frequency(query_list, query_term)

        return (qf_i * (k_2 + 1)) / (k_2 + qf_i)

def calculate_BM25(query_list, query_term, document_rank, inverted_index=None, document_lengths=None):
    """Calculates the BM25 scores given a query term
    :param query_list: The list of query terms seperated by a space
    :param query_term: The term used to calculate the BM25 score
    :param document_rank: a dictionary of documents based on their webpage name and ranking score
    :param inverted_index: the inverted index
    :param document_lengths: a dictionary of document lengths"""
    unique_webpages = get_document_list(inverted_index)
    binary_independence = BinaryIndependence(inverted_index=inverted_index)
    doc_weights = DocWeights(inverted_index=inverted_index, document_lengths=document_lengths)
    query_term_weights = QueryTermWeights()

    #calculate binary independence value
    b_i_value = binary_independence.find_binary_independence_value(query_term)
    #print("Binary independence value: ", b_i_value)

    #calculate query term weight value
    q_t_w_value = query_term_weights.find_query_term_weight(query_list, query_term)
    #print("Query term weight: ", q_t_w_value)

    for web_page in unique_webpages:
        d_w_value = doc_weights.find_doc_weight(query_term, web_page)
        #print(f"{query_term} | {web_page}:    Document weight: ", d_w_value)

        BM25_score = b_i_value * d_w_value * q_t_w_value
        try:
            document_rank[web_page] += BM25_score
        except KeyError:
            document_rank[web_page] = BM25_score

    return document_rank

def welcome_screen():
    """A welcome screen presented to users"""
    print("""Hello and Welcome to the BM25 Search Engine! 
    Some background processes are occurring, but you should soon be able to 
    query to your hearts content""")

def generator_list(list_input):
    """A generator used to format the output of a two value tuple contained in a list
    :param list_input: The list to format"""
    for entry in list_input:
        yield f"'{entry[0]}': Score '{entry[1]}'"

def main():
    import time
    welcome_screen()
    get_average_document_length() #by doing this process early on, we can save repeated computational use later on
    pre_compute_document_length() #by doing this process early, we can speed up the time it takes for the program to work
    inverted_index = pickle.load(open("../crawl_and_index/inverted_index_3.pkl", "rb"))  # open the index
    document_lengths = pickle.load(open("bm25_document_lengths.pkl", "rb"))  #preload the document lengths

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
        document_rank = calculate_BM25(query_list=query_terms_stopped, query_term = term, document_rank=document_rank, inverted_index=inverted_index, document_lengths=document_lengths)

    document_rank = sorted(document_rank.items(), key=lambda x: x[1], reverse=True) #sort the documents by BM25 score
    end_time = start_time - time.time()
    results_generator = generator_list(document_rank)

    print(f"Search took {end_time:,.2f} seconds| The top results are:")
    while True:
        for i in range(10):
            print (next(results_generator))

        more_results = bool(input("\nDo you want more results? Type 'yes' or leave blank"))
        if not more_results:
            break

if __name__ == '__main__':
    main()