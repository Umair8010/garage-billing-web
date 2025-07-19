from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from datetime import datetime
import os

app = Flask(__name__)

# Ensure bills directory exists
BILLS_DIR = os.path.join(os.getcwd(), "bills")
os.makedirs(BILLS_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        customer_name = request.form["customer_name"].strip()
        customer_phone = request.form["customer_phone"].strip()
        services = request.form.getlist("service[]")
        amounts = request.form.getlist("amount[]")

        service_data = []
        for name, amt in zip(services, amounts):
            try:
                price = float(amt)
                service_data.append((name.strip(), price))
            except:
                continue

        total_amount = sum(p for _, p in service_data)
        date_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"bill_{customer_name.replace(' ', '_')}_{date_stamp}.pdf"
        file_path = os.path.join(BILLS_DIR, filename)

        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        margin = 10 * mm
        c.setStrokeColor(colors.darkgray)
        c.setLineWidth(2)
        c.rect(margin, margin, width - 2 * margin, height - 2 * margin)

        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(colors.HexColor("#00BFFF"))
        c.drawString(30 * mm, height - 30 * mm, "Hashu Motor Garage")

        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        c.drawString(30 * mm, height - 36 * mm, "Garage Address")
        c.drawString(30 * mm, height - 42 * mm, "Chalisgoan Road, Kannad - 431103")

        c.setFont("Helvetica-Bold", 14)
        c.drawString(150 * mm, height - 30 * mm, "INVOICE")
        c.setFont("Helvetica", 10)
        c.drawString(150 * mm, height - 42 * mm, datetime.now().strftime("%d-%m-%Y"))

        c.setFont("Helvetica-Bold", 11)
        c.drawString(30 * mm, height - 60 * mm, "BILLED TO")
        c.setFont("Helvetica", 10)
        c.drawString(30 * mm, height - 67 * mm, customer_name)
        c.drawString(30 * mm, height - 74 * mm, customer_phone)

        c.setFont("Helvetica-Bold", 11)
        c.drawString(30 * mm, height - 90 * mm, "SERVICE NAME")
        c.drawString(120 * mm, height - 90 * mm, "AMOUNT (₹)")

        c.setFont("Helvetica", 10)
        y = height - 100 * mm
        for service, price in service_data:
            c.drawString(30 * mm, y, service)
            c.drawString(120 * mm, y, f"₹ {price:.2f}")
            y -= 8 * mm

        y -= 10 * mm
        c.setFont("Helvetica-Bold", 12)
        c.drawString(30 * mm, y, "INVOICE TOTAL")
        c.drawRightString(170 * mm, y, f"₹ {total_amount:.2f}")

        c.setFont("Helvetica-Oblique", 9)
        c.drawString(30 * mm, 20 * mm, "Thank you for choosing Hashu Motor Garage!")
        c.save()

        return send_file(file_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)