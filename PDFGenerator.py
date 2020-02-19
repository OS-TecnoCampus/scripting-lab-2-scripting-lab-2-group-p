from fpdf import FPDF

# setting up the pdf configuration
pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.add_page()
pdf.set_font("Arial", size=12)

# setting up the cover line
pdf.set_line_width(4)
pdf.set_draw_color(255, 200, 0)
pdf.line(30, 275, 30, 10)

# setting up the cover image
pdf.image("resources/tecnocampus.png", x=140, y=50, w=60) # MIRAR

# setting up the rest of the cover
f = open("resources/cover.txt", "r") # MIRAR
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
        elif counter == 4:                  # estos tres if quizas podrian hacerse mejor con un cell
            pdf.set_font("Arial", 'B', 8)
            pdf.text(40, 254, line)
        elif counter == 5:
            pdf.text(0, 258, line)
        else:
            pdf.text(0, 262, line)
        counter = counter + 1

# Tengo que mirar bien como coger una path porque lo que he encontrado no ha funcionado



pdf.output('test.pdf')
