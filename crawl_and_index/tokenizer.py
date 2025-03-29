# imports necessary libraries
from bs4 import BeautifulSoup
from nltk.stem import *
from langdetect import detect
import re
import os


def clean_HTML(html_doc):
    """
    This function cleans the HTML file using BeautifulSoup to extract the plain text.
    """
    with open(html_doc, encoding='utf-8', errors='ignore') as doc:  # prevent encoding issues when opening files
        soup = BeautifulSoup(doc, "html.parser")  # faster than html5lib

    for tags in soup(['script', 'style']):
        tags.decompose()  # removes script and style tags

    # extracts text from HTML and returns it as a string
    cleaned_text = soup.get_text(separator=" ")  # separator checks for spacing between tags
    return cleaned_text


def tokenize(text):
    """
    This function tokenizes the text by retaining alphanumeric characters.
    """
    tokens = re.findall(r'\b\w+\b', text.lower())  # tokenize cleaned HTML AND case handling
    return tokens


def stem(tokens):
    """
    This function applies stemming to tokens and stores stems in an array.
    """
    words = " ".join(tokens)
    language = detect(words)
    if language == "en":
        stemmer = PorterStemmer()  # used to stem english tokens
    elif language == "de":
        stemmer = SnowballStemmer("german")  # used to stem german tokens
    elif language == "es":
        stemmer = SnowballStemmer("spanish")  # used to stem spanish tokens
    stemmed_tokens = [stemmer.stem(token) for token in tokens]  # apply stemming to tokens
    return stemmed_tokens


def text_process(html_doc):
    """
    This function processes text in the HTML file and returns the stemmed tokens.
    """
    text = clean_HTML(html_doc)  # extracts text from HTML
    tokens = tokenize(text)  # tokenizes text
    stemmed_tokens = stem(tokens)  # stems tokens; can change how to stem tokens based on language of text
    return tokens, stemmed_tokens  # returns both tokens and stemmed tokens


def process_repository(directory):
    """
    This function applies text processing to the HTML files in a given directory.
    Save both tokenized and stemmed outputs to separate .txt files.
    """
    output_dir = (os.path.join
                  (f"{os.path.basename(directory)}_Processed_Text"))  # create a relative path for the output folder
    os.makedirs(output_dir, exist_ok=True)  # ensure output directory exists

    for file in os.listdir(directory):  # traverses all files in a directory
        if file.endswith('.html'):  # checks for HTML files

            filepath = os.path.join(directory, file)  # construct the full file path for the current html file
            tokens, stemmed_text = text_process(filepath)

            # construct the output file path
            stemmed_file = os.path.join(output_dir, f"{file}_stemmed.txt")

            # Save stemmed text
            with open(stemmed_file, "w", encoding="utf-8") as out:  # write the processed text to a new .txt file
                out.write(" ".join(stemmed_text))  # join the tokens into a space-separated string

def main():
    """
    This function executes tokenizing and stemming on HTML files in specific directories.
    """
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))

    # find directory paths relative to project root

    directories = [
        os.path.join(project_root, "Code/CodePart1-WebCrawler/repository_German_Wikipedia_Test"),
        os.path.join(project_root, "Code/CodePart1-WebCrawler/repository_Spanish_Wikipedia_Test"),
        os.path.join(project_root, "Code/CodePart1-WebCrawler/repository_Wikipedia Test")
        ]

    for directory in directories:
        print(f"Processing HTML files in: {os.path.abspath(directory)}")

        if os.path.exists(directory):
            process_repository(directory)
            print("Process completed!\n")
        else:
            print(f"Error: Directory {directory} not found.")


if __name__ == "__main__":
    main()