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
    try:
        html = render_template("template_pdf.html")
        pdf_io = BytesIO()
        HTML(string=html).write_pdf(pdf_io)
        pdf_io.seek(0)
        return send_file(pdf_io, mimetype="application/pdf", as_attachment=True, download_name="orden_simple.pdf")
    except Exception as e:
        return f"<h3>Error interno del servidor:</h3><pre>{str(e)}</pre>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)