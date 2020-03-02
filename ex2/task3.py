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

    n = int(input("How many verbs do you want to randomly select?"))

    marcatge = random.sample(list(range(0, 118)), n)

    # Pdf formatting

    head = """<head><meta charset="utf-8">
    <style>table{font-family:arial;border-collapse:collapse;}
    h1{font-family:arial;}
    </style></head>"""

    # Complete Table

    answerSheet = """<h1 align = "center">Complete Forms of {0} Irregular Verbs</h1>
                  <table align = "center" border='1'><tr><th>Infinitive</th><th>Past</th>
                  <th>Past Participle</th><th>Catala</th></tr>""".format(n)

    for i in marcatge:
        answerSheet = answerSheet + "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(infinitive[i],
        past[i],pastParticiple[i], catalan[i])

    answerSheet = answerSheet + "</table>"
    pdfkit.from_string(head + answerSheet, "task3Answers.pdf")

    # Partial Table
    quizSheet = """<h1 align = "center">Quiz of {0} Irregular Verbs</h1>
                 <table border='1' align = "center"><tr><th>Infinitive</th><th>Past</th>
                 <th>Past Participle</th><th>Catala</th></tr>""".format(n)

    for i in marcatge:
        c = random.randint(0, 3)

        if c == 0:
            quizSheet = quizSheet+ "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(infinitive[i], "", "", "")
        elif c == 1:
            quizSheet = quizSheet + "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format("", past[i],"", "")
        elif c == 2:
            quizSheet = quizSheet + "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format("","",pastParticiple[i], "")
        else:
            quizSheet = quizSheet + "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format("","","",catalan[i])

    quizSheet = quizSheet + "</table>"
    pdfkit.from_string(head + quizSheet, "task3Quiz.pdf")

if __name__ == "__main__":
    main()
