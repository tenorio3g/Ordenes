import os
from flask import Flask, render_template, request, send_file
from weasyprint import HTML
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("formulario.html")

@app.route("/pdf", methods=["POST"])
def generar_pdf():
    orden = {
        "area": request.form["area"],
        "trabajo": request.form["trabajo"],
        "equipo": request.form["equipo"],
        "fecha": request.form["fecha"],
        "supervisor": request.form["supervisor"]
    }

    html = render_template("pdf_template.html", orden=orden)
    pdf_io = BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)
    return send_file(pdf_io, mimetype="application/pdf", as_attachment=True, download_name="orden.pdf")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
