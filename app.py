import os
from flask import Flask, render_template, request, send_file
from weasyprint import HTML
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("formulario.html")

@app.route("/pdf")
def generar_pdf():
    html = render_template("pdf_template.html")
    pdf_io = BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)
    return send_file(pdf_io, mimetype="application/pdf", as_attachment=True, download_name="orden_simple.pdf")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render asigna el puerto automáticamente
    app.run(host="0.0.0.0", port=port)
