from fpdf import FPDF
import os


class PDF(FPDF):
    def header(self):
        if self.page_no() != 1:
            # Logo
            self.image("resources/tecnocampus.png", 160, 10, 33)
            # Font
            self.set_font("Arial", size=11)
            # Move to the right
            self.cell(80)
            # Title
            self.set_xy(40, 10)
            self.cell(30, 10, 'PYTHON CODE ANALYSIS')
            # Line break
            self.ln(20)

    # Page footer
    def footer(self):
        if self.page_no() != 1:
            # Position at 1.5 cm from bottom
            self.set_y(-20)
            # Arial italic 8
            self.set_font('Arial', '', 11)
            # Page number
            self.cell(0, 10, 'Page ' + str(self.page_no()) + ' | {nb}', 0, 0, 'R')


# setting up the pdf configuration
pdf = PDF(orientation='P', unit='mm', format='A4')
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font("Arial", size=12)

# setting up the cover line
pdf.set_line_width(4)
pdf.set_draw_color(255, 200, 0)
pdf.line(30, 275, 30, 10)

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
            pdf.text(40, 150, line)
        elif counter == 2:
            pdf.text(40, 170, line)
        elif counter == 3:
            pdf.set_font_size(12)
            pdf.text(40, 200, line)
        elif counter == 4:
            pdf.set_font("Arial", 'B', 8)
            pdf.set_xy(40, 254)
            pdf.cell(0, 10, line)
        elif counter == 5:
            pdf.set_xy(40, 258)
            pdf.cell(0, 10, line)
        else:
            pdf.set_xy(40, 262)
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
            pdf.text(40, 20, line)  # Index
        elif counter == 2:
            pdf.text(40, 25, line)  # 1. INTRODUCTION
        elif counter == 3:
            pdf.set_font("Arial", '', 10)
            pdf.text(45, 30, line)  # 1.1 DESCRIPTION
        elif counter == 4:
            pdf.text(45, 35, line)  # 1.2 OBJECTIVES
        elif counter == 5:
            pdf.text(45, 40, line)  # 1.3 STRUCTURE OF THE PROGRAM
        elif counter == 6:
            pdf.set_font("Arial", 'B', 12)
            pdf.text(40, 45, line)  # 2. THE PROGRAMS
            pdf.set_font("Arial", '', 10)
            yCounter = 50
            fileCounter = 1
            for root, dirs, files in os.walk("ex1"):
                for file in files:
                    if file.endswith(".py"):
                        filename = os.path.join(root, file)
                        filename = "2." + str(fileCounter)+ " " + filename.split('\\')[1]
                        pdf.text(45, yCounter, filename)
                        yCounter += 5
                        fileCounter += 1
        elif counter == 7:
            pdf.set_font("Arial", 'B', 12)
            pdf.text(40, yCounter, line)  # 3. SOME STATISTICS
        counter += 1
    f.close()

# generate the first category (introduction)
pdf.add_page()

# finish the PDF
pdf.close()
pdf.output('test.pdf', 'F')
