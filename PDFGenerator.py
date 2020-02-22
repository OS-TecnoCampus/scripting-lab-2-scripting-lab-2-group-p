from fpdf import FPDF
import os


class PDF(FPDF):
    def header(self):
        if self.page_no() != 1:
            # Logo
            self.image("resources/tecnocampus.png", 160, 10, 33)
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


def main(directory):
    directory = "ex1"  # Esto es una prueba, hay que cambiarlo eventualmente

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
    pdf.image("resources/tecnocampus.png", x=140, y=50, w=60)

    # setting up the rest of the cover
    f = open("resources/cover.txt", "r")
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
    f = open("resources/Index.txt", "r")
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
    f = open("resources/introduction.txt", "r")
    if f.mode == "r":
        lines = f.readlines()
        counter = 1
        for line in lines:
            if counter == 1:    # 1.Introduction
                pdf.set_text_color(255, 200, 0)
                pdf.set_font_size(12)
                pdf.write(5, line)
                pdf.ln()
            elif counter == 2:  # 1.1 Description
                pdf.write(5, line)
                pdf.ln()
            elif counter == 3:
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
                pdf.set_font_size(12)
                pdf.write(5, line)
                pdf.ln()
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
                    # Quizas se tendria que comprovar si hay cada cosa y imprimirlo si se
                    # da, se podria hacer con una array de bool importada facilmente
                    pdf.write(5, "      >   " + text)
                    pdf.ln(10)
            elif counter == 8:  # 1.3 Structure of the project
                pdf.add_page()
                pdf.set_text_color(255, 200, 0)
                pdf.set_font("Arial", 'B', 12)
                pdf.write(5, line)
                pdf.ln()
            elif counter == 9:
                pdf.set_font("Arial", '', 10)
                pdf.set_text_color(0)
                pdf.write(5, line)
                pdf.ln()
                # Aqui iria toda la mierda de la generacion de la estructura que aun no se hacer
            counter += 1

    # finish the PDF
    pdf.close()
    pdf.output('test.pdf', 'F')


if __name__ == "__main__":
    main("ex1")     # Lo mismo aqui
