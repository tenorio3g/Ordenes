from flask import Flask, render_template_string, send_file
from weasyprint import HTML
from io import BytesIO

app = Flask(__name__)

# Esta es una orden de ejemplo. Puede remplazarse más adelante por datos dinámicos.
orden_ejemplo = {
    "area": "SNACK",
    "trabajo": "Reemplazar barras dañadas",
    "celda": "Celda 1",
    "requisitor": "Departamento Médico",
    "planta": "Planta A",
    "supervisor": "Celeste Tirado",
    "fecha": "2025-06-10",
    "numero": "62502",
    "solicitante": "MTTO. DE PLANTA",
    "checklist": [
        "Delimitar el área de trabajo",
        "Cubrir máquinas o material",
        "Confirmar permisos",
        "Inspeccionar herramientas",
        "Usar EPP",
        "Verificación de ausencia de energía"
    ],
    "material": "Cables, barras, sujetadores",
    "observaciones": "Trabajo realizado correctamente, se reemplazaron 3 barras.",
    "electroducto": "E-02",
    "espacio": "4",
    "tablero": "T-12",
    "espacio_tab": "6",
    "cable": "THHN 12AWG",
    "canalizacion": "Conduit PVC",
    "obs_electrico": "Todo instalado según norma.",
    "fecha_inicio": "2025-06-10",
    "hora_inicio": "08:00",
    "fecha_fin": "2025-06-10",
    "hora_fin": "10:30",
    "realizado": "Técnico A"
}

@app.route("/")
def index():
    return """
    <h2>Exportar orden de trabajo</h2>
    <a href="/exportar" class="btn btn-primary">Descargar PDF</a>
    """

@app.route("/exportar")
def exportar():
    # Cargar la plantilla HTML
    with open("pdf_template.html", encoding="utf-8") as f:
        template = f.read()

    # Renderizar la plantilla con los datos
    html = render_template_string(template, orden=orden_ejemplo)

    # Convertir HTML a PDF
    pdf_io = BytesIO()
    HTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    return send_file(
        pdf_io,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="orden_trabajo.pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
