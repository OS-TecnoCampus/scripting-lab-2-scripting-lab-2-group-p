from fpdf import FPDF
from code_analyzer.scriptReader import *
import os
import redbaron


class PDF(FPDF):
    def header(self):
        if self.page_no() != 1:
            # Logo
            self.image("../resources/tecnocampus.png", 160, 10, 33)
            # Font
            self.set_font("Arial", size=10)
            # Move to the right
            self.cell(80)
            # Title
            self.set_xy(25, 10)
            self.cell(30, 10, 'PYTHON CODE ANALYSIS')
            # Line break
            self.ln(20)

    # Page footer
    def footer(self):
        if self.page_no() != 1:
            # Position at 1.5 cm from bottom
            self.set_y(-20)
            # Arial italic 8
            self.set_font('Arial', '', 10)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()) + ' | {nb}', 0, 0, 'R')


pdfPages = []  # static variable which will record the number page of every category


def main():
    inputed = False

    while not inputed:
        directory = input("Please type the directory with the python files you want to analyze: ")
        if os.path.isdir(directory):
            inputed = True
        else:
            print("Could not find the specified directory")

    # setting up the pdf configuration
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.set_left_margin(25)
    pdf.set_top_margin(35)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # setting up the cover line
    pdf.set_line_width(4)
    pdf.set_draw_color(255, 200, 0)
    pdf.line(20, 275, 20, 10)

    # setting up the cover image
    pdf.image("../resources/tecnocampus.png", x=140, y=50, w=60)

    # setting up the rest of the cover
    f = open("../resources/Cover.txt", "r")
    if f.mode == "r":
        lines = f.readlines()
        counter = 1
        for line in lines:
            if counter == 1:
                pdf.set_font_size(24)
                pdf.text(30, 150, line)
            elif counter == 2:
                pdf.text(30, 170, line)
            elif counter == 3:
                pdf.set_font_size(12)
                pdf.text(30, 200, line)
            elif counter == 4:
                pdf.set_font("Arial", 'B', 8)
                pdf.set_xy(30, 254)
                pdf.cell(0, 10, line)
            elif counter == 5:
                pdf.set_xy(30, 258)
                pdf.cell(0, 10, line)
            else:
                pdf.set_xy(30, 262)
                pdf.cell(0, 10, line)
            counter += 1
    f.close()

    # creating the index
    pdf.add_page()
    f = open("../resources/Index.txt", "r")
    if f.mode == "r":
        lines = f.readlines()
        counter = 1
        for line in lines:
            if counter == 1:
                pdf.set_font("Arial", 'B', 12)
                pdf.text(25, 35, line)  # Index
            elif counter == 2:
                pdf.text(25, 42, line)  # 1. INTRODUCTION
            elif counter == 3:
                pdf.set_font("Arial", '', 10)
                pdf.text(30, 47, line)  # 1.1 DESCRIPTION
            elif counter == 4:
                pdf.text(30, 52, line)  # 1.2 OBJECTIVES
            elif counter == 5:
                pdf.text(30, 57, line)  # 1.3 STRUCTURE OF THE PROGRAM
            elif counter == 6:
                pdf.set_font("Arial", 'B', 12)
                pdf.text(25, 64, line)  # 2. THE PROGRAMS
                pdf.set_font("Arial", '', 10)
                yCounter = 67
                fileCounter = 1
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file.endswith(".py"):
                            filename = os.path.join(root, file)
                            filename = "2." + str(fileCounter) + " " + filename.split('\\')[1]
                            pdf.set_xy(30, yCounter)
                            pdf.write(5, filename)
                            yCounter += 5
                            fileCounter += 1
            elif counter == 7:
                pdf.set_font("Arial", 'B', 12)
                yCounter += 5
                pdf.text(25, yCounter, line)  # 3. SOME STATISTICS
            counter += 1
    f.close()

    # generate the first category (introduction)
    pdf.add_page()
    f = open("../resources/Introduction.txt", "r")
    if f.mode == "r":
        lines = f.readlines()
        counter = 1
        for line in lines:
            if counter == 1:  # 1.Introduction
                pdf.set_text_color(255, 200, 0)
                pdf.set_font_size(12)
                pdf.write(5, line)
                pdf.ln()
                pdfPages.append("?")
                pdfPages.append(pdf.page_no())
            elif counter == 2:  # 1.1 Description
                pdf.write(5, line)
                pdf.ln()
                pdfPages.append("!")
                pdfPages.append(pdf.page_no())
            elif counter == 3:  # Files of the project
                pdf.set_font("Arial", '', 10)
                pdf.set_text_color(0)
                pdf.write(5, line.split('!')[0] + directory + line.split('!')[1])
                pdf.ln()
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file.endswith(".py"):
                            filename = os.path.join(root, file)
                            filename = "    >   " + filename.split('\\')[1]
                            pdf.set_font("Arial", 'B', 10)
                            pdf.write(5, filename)
                            pdf.ln(10)
            elif counter == 4:  # 1.2 Objectives
                pdf.ln()
                pdf.set_text_color(255, 200, 0)
                pdf.set_font("Arial", 'B', 12)
                pdf.write(5, line)
                pdf.ln()
                pdfPages.append(pdf.page_no())
            elif counter == 5:
                pdf.set_font("Arial", '', 10)
                pdf.set_text_color(0)
                pdf.write(5, line)
                pdf.ln()
            elif counter == 6:
                pdf.write(5, line)
                pdf.ln()
            elif counter == 7:
                pdf.set_font("Arial", 'B', 10)
                for text in line.split('!'):
                    pdf.write(5, "      >   " + text)
                    pdf.ln(10)
            elif counter == 8:  # 1.3 Structure of the project
                pdf.add_page()
                pdf.set_text_color(255, 200, 0)
                pdf.set_font("Arial", 'B', 12)
                pdf.write(5, line)
                pdf.ln()
                pdfPages.append(pdf.page_no())
            elif counter == 9:
                pdf.set_font("Arial", '', 10)
                pdf.set_text_color(0)
                pdf.write(5, line)
                pdf.ln(10)
                graphGenerator(directory)
                pdf.image("../resources/graph.png", x=30, y=50, w=150)
            counter += 1
    f.close()

    # generate the second category (programs)
    pdf.add_page()
    f = open("../resources/Programs.txt", "r")
    if f.mode == "r":
        lines = f.readlines()
        pdf.set_text_color(255, 200, 0)
        pdf.set_font("Arial", 'B', 12)
        pdf.write(5, "2. The programs")  # 2. The programs
        pdfPages.append("?")
        pdfPages.append(pdf.page_no())
        pdfPages.append("!")
        pdf.ln(10)
        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0)
        pdf.write(5, "The list of the programs of the project is detailed in the next section")
        pdf.ln(10)

        fileCounter = 1
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    pdf.set_text_color(255, 200, 0)
                    pdf.set_font("Arial", 'B', 12)
                    filename = os.path.join(root, file)
                    filename = "2." + str(fileCounter) + " " + filename.split('\\')[1]
                    pdfPages.append(pdf.page_no())
                    pdf.write(5, filename)
                    pdf.ln(10)
                    pdf.set_font("Arial", '', 10)
                    pdf.set_text_color(0)
                    f.seek(0)
                    with open(os.path.join(root, file), "r") as f2:
                        red = redbaron.RedBaron(f2.read())
                        counter = 1
                        for line in lines:
                            pdf.set_font("Arial", '', 10)
                            pdf.write(5, line)
                            pdf.ln()
                            pdf.set_font("Arial", 'B', 10)
                            if counter == 1:
                                libraries = importedLibraries(red)
                                if not libraries:
                                    pdf.write(5, "  >   There are no imported libraries")
                                    pdf.ln()
                                else:
                                    for lib in libraries:
                                        pdf.write(5, lib)
                                        pdf.ln(5)
                            elif counter == 2:
                                functions = definedFunctions(red)
                                if not functions:
                                    pdf.write(5, "  >   There are no defined functions")
                                    pdf.ln()
                                else:
                                    for fun in functions:
                                        pdf.write(5, fun)
                                        pdf.ln(5)
                            elif counter == 3:
                                comments = commentsOnCode(red)
                                if not comments:
                                    pdf.write(5, "  >   There are no comments in the code")
                                    pdf.ln()
                                else:
                                    for com in comments:
                                        pdf.write(5, com)
                                        pdf.ln(5)
                            elif counter == 4:
                                variables = usedVariables(red)
                                if not variables:
                                    pdf.write(5, "  >   There are no defined or used variables in the code")
                                    pdf.ln()
                                else:
                                    for var in variables:
                                        pdf.write(5, "  >   " + str(var.name))
                                        pdf.ln()
                                        pdf.write(5, "      -   First use in line " + str(var.line))
                                        pdf.ln()
                                        pdf.write(5, "      -   Next uses:")
                                        pdf.ln()
                                        if var.reassignment:
                                            string = "          #   Reassignment: line "
                                            count = 0
                                            for re in var.reassignment:
                                                if count < len(var.reassignment):
                                                    string += str(re) + ", "
                                                else:
                                                    string += str(re)
                                                count += 1
                                            pdf.write(5, string)
                                            pdf.ln()
                                        if var.use:
                                            string = "          #   Use: line "
                                            count = 0
                                            for used in var.use:
                                                if count < len(var.use):
                                                    string += str(used) + ", "
                                                else:
                                                    string += str(used)
                                                count += 1
                                            pdf.write(5, string)
                                            pdf.ln()
                                        if var.with_functions:
                                            pdf.write(5, "          #   With functions:")
                                            pdf.ln()
                                            for fun in var.with_functions:
                                                pdf.write(5, "              ->  " + str(fun))
                                                pdf.ln()
                                        if var.operators:
                                            pdf.write(5, "          #   Operators:")
                                            pdf.ln()
                                            for op in var.operators:
                                                pdf.write(5, "              ->  " + op)
                                                pdf.ln()
                                        pdf.ln(5)
                            elif counter == 5:
                                functions = usedFunctions(red)
                                if not functions:
                                    pdf.write(5, "  >   There are no defined or used functions in the code")
                                    pdf.ln()
                                else:
                                    cn = 0
                                    for fn in functions:
                                        if cn == 0:
                                            for fromFunctions in fn:
                                                cn2 = 0
                                                for ln in fromFunctions:
                                                    if cn2 == 0:
                                                        pdf.write(5, "  >   From " + ln + ":")
                                                        pdf.ln()
                                                    else:
                                                        pdf.write(5, "      -   " + ln)
                                                        pdf.ln()
                                                    cn2 += 1
                                        elif cn == 1:
                                            pdf.write(5, "  >   Generic:")
                                            pdf.ln()
                                            for generics in fn:
                                                pdf.write(5, "      -   " + generics)
                                                pdf.ln()
                                        elif cn == 2:
                                            for withVariable in fn:
                                                cn2 = 0
                                                for ln in withVariable:
                                                    if cn2 == 0:
                                                        pdf.write(5, "  >   With variable " + ln + ":")
                                                        pdf.ln()
                                                    else:
                                                        pdf.write(5, "          -   " + ln)
                                                        pdf.ln()
                                                    cn2 += 1
                                        cn += 1
                            counter += 1
                            pdf.ln(5)
                    pdf.ln(10)
                    fileCounter += 1
    f.close()

    # generate the third category (statistics)
    pdf.add_page()
    f = open("../resources/Statistics.txt", "r")
    if f.mode == "r":
        lines = f.readlines()
        counter = 1
        for line in lines:
            if counter == 1:
                pdf.set_text_color(255, 200, 0)
                pdf.set_font("Arial", 'B', 12)
                pdf.write(10, line)  # 3. Some statistics
                pdfPages.append("?")
                pdfPages.append(pdf.page_no())
            elif counter == 2:
                pdf.set_font("Arial", '', 10)
                pdf.set_text_color(0)
                fileCounter = 0
                functionCounter = 0
                lineCounter = 0
                variableCounter = countVariables(directory)
                libraryCounter = countLibraries(directory)
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file.endswith(".py"):
                            fileCounter += 1
                            with open(os.path.join(root, file), "r") as f2:
                                red = redbaron.RedBaron(f2.read())
                                functionCounter += countFunctions(red)
                                lineCounter += countLines(os.path.join(root, file))
                            f2.close()
                pdf.write(5, line.split("!")[0] + str(fileCounter) + line.split("!")[1] + str(functionCounter) +
                          line.split("!")[2] + str(variableCounter) + line.split("!")[3] + str(libraryCounter) +
                          line.split("!")[4] + str(lineCounter) + line.split("!")[5])
            counter += 1
    f.close()

    # reformatting the index
    lastPage = pdf.page
    pdf.page = 2
    y = 42
    yCounter = 7
    for page in pdfPages:
        if str(page) == "!":
            yCounter = 5
            pdf.set_font("Arial", '', 10)
        elif str(page) == "?":
            yCounter = 7
            pdf.set_font("Arial", 'B', 10)
        else:
            pdf.set_font("Arial", 'B', 10)
            pdf.text(185, y, "pg " + str(page))
            y += yCounter
    pdf.page = lastPage

    # finish the PDF
    pdf.output('../Report_TCM.pdf', 'F')
    pdf.close()


if __name__ == "__main__":
    main()
