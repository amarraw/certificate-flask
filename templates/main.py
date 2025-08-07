from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        pdf_path = generate_certificate(name)
        return send_file(pdf_path, as_attachment=True)
    return render_template('form.html')


def generate_certificate(name):
    pdf = FPDF('L', 'mm', 'A4')  # Landscape A4
    pdf.add_page()

    # Add background image (full size)
    pdf.image("back2.png", x=0, y=0, w=297, h=210)

    # Set font
    pdf.set_font("Helvetica", 'B', 28)
    pdf.set_text_color(0, 0, 0)

    # Calculate text width and center it
    text_width = pdf.get_string_width(name)
    page_width = 297  # A4 Landscape width in mm
    x_position = (page_width - text_width) / 2
    y_position = 90  # Adjust based on your image

    # Add the name centered
    pdf.set_xy(x_position, y_position)
    pdf.cell(text_width + 2, 4, name)

    # Output file
    filename = f"{name}_certificate.pdf"
    pdf.output(filename)
    return filename


if __name__ == '__main__':
    app.run()
