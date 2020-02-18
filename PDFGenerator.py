from fpdf import FPDF
import os

# setting up the pdf configuration
pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.set_font("Arial", size=12)

# setting up the cover line
pdf.set_line_width(4)
pdf.set_draw_color(255, 200, 0)
pdf.line(30, 275, 30, 10)

#setting up the cover image
script_dir = os.path.dirname(__file__)
image_path = "../resources/tecnocampus.png"
file_path = os.path.join(script_dir, image_path)
pdf.image("C:/Users/Joel/PycharmProjects/scripting-lab-2-scripting-lab-2-group-p/resources/tecnocampus.png", x=140, y=50, w=60) # MIRAR

pdf.output('test.pdf')
