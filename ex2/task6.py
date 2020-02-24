import matplotlib.pyplot as plt
import collections
import requests
import wordcloud
from bs4 import BeautifulSoup


# Function definitions

# Saves the verbs found in soup object into a dictionary


def read_store_verbs(soup):
    dictionary = {}

    for readStrings, string in enumerate(soup.stripped_strings):
        if 6 < readStrings < 362:
            add_to_dict(string, dictionary)

    return dictionary


# Adds a string as key to a given dictionary, with a 0 value

def add_to_dict(string, dictionary):
    if string != "BEEN ABLE TO" and len(string.split()) > 1:  # verb has more than one form
        for form in string.split():  # we separate the forms
            form = form.upper()
            form = form.strip("(").strip(")").strip(",")
            if form != "OR":
                dictionary[form] = 0
    else:
        if string != "(US)":  # we exclude annotation
            dictionary[string.upper()] = 0


# Counts words per line and number of appearances/word


def process_document(doc, d, l):
    nWords = 0

    for line in doc:
        for word in line.split():
            nWords = nWords + 1  # count number of words in this line
            word = word.upper()
            if word in d:
                d[word] += 1
        l.append(nWords)
        nWords = 0  # we reset the number of words for the next line


# Generates and saves to a file a histogram for words/line in a document, given the data, title and output file
def generate_histogram(data, title, output):
    plt.hist(data, bins=100)
    plt.xlabel("Words")
    plt.ylabel("Lines")
    plt.title(title)
    plt.savefig(output)
    plt.clf()  # Clear figure after storing it so the next one can be drawn


# Generates and saves a word cloud to a file, given a dictionary with word data, user prompt and output file
def generate_wordcloud(dictionary, prompt, output):
    n = int(input(prompt))

    firstpairs = collections.Counter({k: c for k, c in dictionary.items() if c > 0}).most_common(n)
    firstpairs = dict(firstpairs)

    docCloud = wordcloud.WordCloud().generate_from_frequencies(firstpairs)
    wordcloud.WordCloud.to_file(docCloud, output)


# End function definitions

def main():
    # Verb info

    verbInfo = "http://www.xtec.cat/~mcerda1/altres/verbs%20irregulars.htm"
    verbDoc = requests.get(verbInfo).text

    # Document 1
    # We retrieve the verbs and store them for later use
    verbs = read_store_verbs(BeautifulSoup(verbDoc, "html.parser"))

    doc1 = "https://www.acc.umu.se/~coppelia/pooh/stories/ch1.html"
    r = requests.get(doc1)
    document1 = BeautifulSoup(r.text, "html.parser")

    wordsLine = []
    process_document(document1.stripped_strings, verbs, wordsLine)

    # Histogram
    generate_histogram(wordsLine, "Histogram with Words/Line in Document 1", "doc1histogram.png")

    # Word cloud
    generate_wordcloud(verbs, "For document 1, what number of most frequent irregular verbs would you like to compute?",
                       "doc1Wordcloud.png")

    # Document 2
    # We retrieve the verbs and store them for later use
    verbs = read_store_verbs(BeautifulSoup(verbDoc, "html.parser"))

    doc2 = "https://www.ted.com/talks/subtitles/id/2464/lang/eng"
    r = requests.get(doc2)
    document2 = BeautifulSoup(r.text, "html.parser")

    wordsLine = []
    lines = []

    s = document2.text
    for content in s.split(sep='"content":"'):
        if '","startOfParagraph"' in content:
            content = content.replace(r'\n', '\n').replace(r'\"', '"').replace(r"\u00fc", "\u00fc").replace(r"\u00e9",
                                                                                                            "\u00e9")
            # we replace raw line breaks so that they will be shown, remove \ around quotes, and replace raw unicode
            lines.append('","startOfParagraph"'.join(content.split('","startOfParagraph"')[:-1]))

    process_document(lines, verbs, wordsLine)
    # Histogram
    generate_histogram(wordsLine, "Histogram with Words/Line in Document 2", "doc2histogram.png")

    # Word cloud
    generate_wordcloud(verbs, "For document 2, what number of most frequent irregular verbs would you like to compute?",
                       "doc2Wordcloud.png")


if __name__ == "__main__":
    main()
