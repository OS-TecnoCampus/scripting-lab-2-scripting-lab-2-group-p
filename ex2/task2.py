import requests
import random
import pdfkit
from bs4 import BeautifulSoup


def main():
    verbInfo = "http://www.xtec.cat/~mcerda1/altres/verbs%20irregulars.htm"
    verbDoc = requests.get(verbInfo).text
    soup = BeautifulSoup(verbDoc, "html.parser")

    # We retrieve the verbs and store them for later use
    infinitive = []
    past = []
    pastParticiple = []
    catalan = []

    for readStrings, string in enumerate(soup.stripped_strings):
        if readStrings > 6 and string != "(US)":
            if readStrings < 125:
                infinitive.append(string)
            elif readStrings < 243:
                past.append(string)
            elif readStrings < 362:
                if string == "GOTTEN":
                    string.append("(US)")
                pastParticiple.append(string)
            elif readStrings < 480:
                catalan.append(string)

    # Pdf formatting

    head = """<head><meta charset="utf-8">
    <style>table{font-family:arial;border-collapse:collapse;}
    h1{font-family:arial;}
    </style></head>"""

    verblists = []
    numVerbs = 118

    n = 0
    while n < numVerbs:
        userinput = int(input("Please, enter a positive number:"))
        verblists.append(userinput)
        n = n + userinput

    if n > numVerbs:  # if the last number given by the user is larger than the number of verbs remaining, we adjust it
        n = n - numVerbs
        verblists[len(verblists) - 1] = verblists[len(verblists) - 1] - n

    lastVerb = 0
    for index, number in enumerate(verblists):

        answerSheet = """<h1 align = "center">Complete Forms of {0} Irregular Verbs</h1>
                <table align = "center" border='1'><tr><th>Infinitive</th><th>Past</th>
                <th>Past Participle</th><th>Catala</th></tr>""".format(number)

        quizSheet = """<h1 align = "center">Quiz of {0} Irregular Verbs</h1>
                    <table border='1' align = "center"><tr><th>Infinitive</th><th>Past</th>
                    <th>Past Participle</th><th>Catala</th></tr>""".format(number)

        for x in range(lastVerb, lastVerb + number):
            # Complete Table
            answerSheet = answerSheet + "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(
                infinitive[x], past[x], pastParticiple[x], catalan[x])

            # Partial Table

            c = random.randint(0, 3)

            if c == 0:
                quizSheet = quizSheet + "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(
                    infinitive[x],
                    "", "", "")
            elif c == 1:
                quizSheet = quizSheet + "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format("", past[x],
                                                                                                           "",
                                                                                                           "")
            elif c == 2:
                quizSheet = quizSheet + "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format("", "",
                                                                                                           pastParticiple[
                                                                                                               x], "")
            else:
                quizSheet = quizSheet + "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format("", "", "",
                                                                                                           catalan[x])

        answerSheet = answerSheet + "</table>"
        quizSheet = quizSheet + "</table>"
        pdfkit.from_string(head + answerSheet, "task2List{0}Answers.pdf".format(index + 1))
        pdfkit.from_string(head + quizSheet, "task2List{0}Quiz.pdf".format(index + 1))
        lastVerb += number


if __name__ == "__main__":
    main()
