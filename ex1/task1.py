import pdfkit
import requests


def main():
    url = "http://www.xtec.cat/~mcerda1/altres/verbs%20irregulars.htm"
    r = requests.get(url)  # get the information from the url

    html = r.text.replace("<marquee>", "").replace("</marquee>", "").replace("windows-1252", "utf-8")
    # we get the text from the url, then remove the marquee from the original document
    # and change the encoding to make sure special characters get rendered properly in the pdf

    pdfkit.from_string(html, "irregularVerbs.pdf")  # generate the pdf


if __name__ == "__main__":
    main()
