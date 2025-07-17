from flask import Flask, render_template, request, make_response
import pdfkit
from PyPDF2 import PdfReader, PdfWriter
import os

app = Flask(__name__)

CHECKLIST_ITEMS = [
    "Delimitar el área de Trabajo",
    "Cubrir con plástico, máquinas o material de producción",
    "Confirmar con el permiso de trabajo antes de iniciar actividades",
    "Inspeccionar la herramienta y equipo a utilizar que se encuentren en buenas condiciones",
    "Hacer uso obligatorio del Equipo de Seguridad Personal EPP",
    "Identificar Alimentación Eléctrica para Candadean en caso de ser necesario",
    "Comprobar 100% la Ausencia de Energía con Amperímetro en todos los puntos",
    "Puntos de alimentación energías acumuladas, entradas, salidas y retornos",
    "Realizar todas las maniobras en base a seguridad",
    "Limpiar el área después de realizado el trabajo",
    "Reportar condiciones del área y equipos en cuanto a la conclusión del trabajo realizado"
]

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/exportar_pdf', methods=['POST'])
def exportar_pdf():
    orden = {
        'area': request.form.get('area'),
        'trabajo': request.form.get('trabajo'),
        'celda': request.form.get('celda'),
        'requisitor': request.form.get('requisitor'),
        'planta': request.form.get('planta'),
        'supervisor': request.form.get('supervisor'),
        'fecha_requisicion': request.form.get('fecha_requisicion'),
        'orden': request.form.get('orden'),
        'fecha_inicio': request.form.get('fecha_inicio'),
        'hora_inicio': request.form.get('hora_inicio'),
        'fecha_fin': request.form.get('fecha_fin'),
        'hora_fin': request.form.get('hora_fin'),
        'realizado_por': request.form.get('realizado_por'),
        'material': request.form.get('material'),
        'observaciones': request.form.get('observaciones'),
        'electroducto': request.form.get('electroducto'),
        'espacio_electroducto': request.form.get('espacio_electroducto'),
        'num_tablero': request.form.get('num_tablero'),
        'espacio_tablero': request.form.get('espacio_tablero'),
        'cable': request.form.get('cable'),
        'canalizacion': request.form.get('canalizacion'),
        'obs_electrica': request.form.get('obs_electrica'),
        'check': request.form.getlist('check[]')
    }

    rendered = render_template('pdf_template.html', data=orden, checklist=CHECKLIST_ITEMS)

    options = {
        'page-width': '11in',
        'page-height': '8.5in',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'encoding': 'UTF-8',
        'no-outline': None
    }

    # 1️⃣ Genera PDF temporal vertical
    temp_pdf = "temp_orden.pdf"
    pdfkit.from_string(rendered, temp_pdf, options=options)

    # 2️⃣ Rota el PDF con PyPDF2
    rotated_pdf = "orden_trabajo_rotated.pdf"
    reader = PdfReader(temp_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(90)
        writer.add_page(page)

    with open(rotated_pdf, "wb") as f_out:
        writer.write(f_out)

    # 3️⃣ Devuelve PDF girado
    with open(rotated_pdf, "rb") as f:
        pdf_data = f.read()

    response = make_response(pdf_data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=orden_trabajo.pdf'

    # Limpieza opcional
    os.remove(temp_pdf)
    os.remove(rotated_pdf)

    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
