import requests
import pdfkit
import collections
from bs4 import BeautifulSoup


# Function definitions

# Saves the verbs found in soup object into the specified dictionaries


def read_store_verbs(infinitive, past, pastParticiple, soup):
    for readStrings, string in enumerate(soup.stripped_strings):
        if readStrings > 6:
            if readStrings < 125:
                add_to_dict(string, infinitive)
            else:
                if readStrings < 243:
                    add_to_dict(string, past)
                else:
                    if readStrings < 362:
                        add_to_dict(string, pastParticiple)


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


# Generates string with html for a two-column table, table header not included


def generate_table(items):
    string = ""

    for k, v in items:
        string = string + "<tr><td>{0}</td><td>{1}</td></tr>".format(k, v)

    string = string + "</table>"
    return string


# End function definitions


def main():
    url = "https://www.ted.com/talks/subtitles/id/2464/lang/eng"
    verbInfo = "http://www.xtec.cat/~mcerda1/altres/verbs%20irregulars.htm"

    verbDoc = requests.get(verbInfo).text

    # We retrieve the verbs and store them for later use
    infinitive = collections.OrderedDict()
    past = collections.OrderedDict()
    pastPart = collections.OrderedDict()
    read_store_verbs(infinitive, past, pastPart, BeautifulSoup(verbDoc, "html.parser"))

    # We compute statistics about the document
    r = requests.get(url)
    document = BeautifulSoup(r.text, "html.parser")

    nWords = 0
    wordTotal = 0
    wordsLine = {}

    # We process the document to get the text

    lines = []
    s = document.text
    for content in s.split(sep='"content":"'):
        if '","startOfParagraph"' in content:
            content = content.replace(r'\n', '\n').replace(r'\"', '"').replace(r"\u00fc", "\u00fc").replace(r"\u00e9",
                                                                                                            "\u00e9")
            # we replace raw line breaks so that they will be shown, remove \ around quotes, and replace raw unicode
            lines.append('","startOfParagraph"'.join(content.split('","startOfParagraph"')[:-1]))

    for index, line in enumerate(lines):
        for word in line.split():
            nWords = nWords + 1  # count number of words in this line
            word = word.upper()
            if word in infinitive:
                infinitive[word] += 1
            if word in past:
                past[word] += 1
            if word in pastPart:
                pastPart[word] += 1
        wordsLine[index] = [line, nWords]
        wordTotal = wordTotal + nWords  # add words in the line to total
        nWords = 0  # we reset the number of words for the next line

    n = int(input("What number of most frequent irregular verbs would you like to compute?"))

    verbs = {}
    verbs.update(infinitive)
    verbs.update(past)
    verbs.update(pastPart)

    firstNpairs = collections.Counter(verbs).most_common(n)

    # GENERATE OUTPUT

    # Number of words per line
    tableLineWords = """<br><br><h2 align="center">Number of words per line</h2><table align="center" border='1'>
    <tr><th>Line Number</th><th>Line Content</th><th>Word Count</th></tr>"""

    for k, v in wordsLine.items():
        tableLineWords = tableLineWords + "<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>".format(k, v[0], v[1])

    tableLineWords = tableLineWords + "</table><br><br>"

    # List of verbs and appearances

    verbTable = """<h2 align="center">Number of irregular verbs</h2><table class = "verbTable" border='1'>
    <tr><th>Infinitive Verb</th><th>Appearances</th></tr>""" + generate_table(infinitive.items()) + """
    <table class ="verbTable" border='1'><tr><th>Past Verb</th><th>Appearances</th></tr>""" + generate_table(
        past.items()) + """
    <table class = "verbTable" border='1'><tr><th>Past Participle Verb</th><th>Appearances</th></tr>
    """ + generate_table(pastPart.items())

    # Most frequent verbs
    topN = """<div align = "center" class="topVerbs"><h2>{0} most frequent irregular verbs</h2><table border='1'>
    <tr><th>Verb</th><th>Number of occurrences</th></tr>""".format(n) + generate_table(firstNpairs) + "</div>"

    css = """<head><meta charset="utf-8">
    <style>table{font-family:arial;border-collapse:collapse;}
    .verbTable{float:left;width:33%;}
    .topVerbs{display:inline-block;width:100%;}
    h1,h2{font-family:arial;}
    </style></head>"""

    outputText = """
    <h1 align ="center">Document Statistics</h1>
    <h2>Number of lines in the document: {0}</h2>
    <h2>Number of words in the document: {1}</h2>
    """.format(len(wordsLine), wordTotal) + tableLineWords + verbTable + topN

    pdfkit.from_string(css + outputText, "task5.pdf")


if __name__ == "__main__":
    main()
