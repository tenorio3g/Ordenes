from flask import Flask, send_file
from weasyprint import HTML
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def index():
    return '''
    <html>
      <head><title>Generador de PDF</title></head>
      <body style="font-family:Arial; text-align:center; margin-top:50px;">
        <h1>Exportar Orden de Trabajo</h1>
        <a href="/pdf" style="padding:10px 20px; background-color:green; color:white; text-decoration:none;">Exportar a PDF</a>
      </body>
    </html>
    '''

@app.route("/pdf")
def generar_pdf():
    html = """
    <html>
      <head><meta charset='utf-8'></head>
      <body>
        <h1 style="text-align:center;">Orden de Trabajo</h1>
        <p>Esta es una prueba simple para exportar un PDF desde Flask y WeasyPrint.</p>
        <p><b>Área:</b> Empaque</p>
        <p><b>Trabajo:</b> Revisión de ductos</p>
        <p><b>Supervisor:</b> Celeste Tirado</p>
      </body>
    </html>
    """

    pdf_io = BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    return send_file(
        pdf_io,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="orden_simple.pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
