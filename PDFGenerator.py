from fpdf import FPDF


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
            # pdf.text(40, 150, line)
            pdf.set_xy(40, 150)
            pdf.cell(0, 10, line)
        elif counter == 2:
            pdf.set_xy(40, 170)
            pdf.cell(0, 10, line)
            # pdf.text(40, 170, line)
        elif counter == 3:
            pdf.set_font_size(12)
            # pdf.text(40, 200, line)
            pdf.set_xy(40, 200)
            pdf.cell(0, 10, line)
        elif counter == 4:  # estos tres if quizas podrian hacerse mejor con un cell
            pdf.set_font("Arial", 'B', 8)
            # pdf.text(40, 254, line)
            pdf.set_xy(40, 254)
            pdf.cell(0, 10, line)
        elif counter == 5:
            pdf.set_xy(40, 258)
            pdf.cell(0, 10, line)
            # pdf.text(0, 258, line)
        else:
            pdf.set_xy(40, 262)
            pdf.cell(0, 10, line)
            # pdf.text(0, 262, line)
        counter += 1
f.close()

pdf.add_page()

pdf.close()
pdf.output('test.pdf', 'F')
