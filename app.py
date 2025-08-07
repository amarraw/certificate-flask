from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os
import werkzeug.utils

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        pin = request.form.get('pin', '').strip()
        feedback = request.form.get('feedback', '').strip()

        CORRECT_PIN = "1234"

        if not name:
            return render_template('form.html', error="Name is required.")
        if pin != CORRECT_PIN:
            return render_template('form.html', error="Invalid PIN.")

        # Logging the extra fields (for your reference)
        print(f"Certificate requested by: {name}, Email: {email}, Phone: {phone}, Feedback: {feedback}")

        safe_name = werkzeug.utils.secure_filename(name)
        pdf_path = generate_certificate(safe_name, email, phone)
        response = send_file(pdf_path, as_attachment=True, download_name=f"{safe_name}_certificate.pdf")
        try:
            os.remove(pdf_path)
        except Exception:
            pass
        return response
    return render_template('form.html')


def generate_certificate(name, email, phone):
    pdf = FPDF('L', 'mm', 'A4')  # Landscape A4
    pdf.add_page()

    # Background image
    pdf.image("back2.png", x=0, y=0, w=297, h=210)

    # Name
    pdf.set_font("Helvetica", 'B', 28)
    pdf.set_text_color(0, 0, 0)
    text_width = pdf.get_string_width(name)
    x_position = (297 - text_width) / 2
    pdf.set_xy(x_position, 90)
    pdf.cell(text_width + 2, 10, name)

    # Add email and phone
    pdf.set_font("Helvetica", '', 16)
    pdf.set_text_color(60, 60, 60)
    pdf.set_xy(10, 160)
    pdf.cell(0, 10, f"Email: {email}")
    pdf.set_xy(10, 170)
    pdf.cell(0, 10, f"Phone: {phone}")

    filename = f"{name}_certificate.pdf"
    pdf.output(filename)
    return filename


if __name__ == '__main__':
    app.run(debug=True)
