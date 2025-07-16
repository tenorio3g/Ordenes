from flask import Flask, render_template, request, make_response
import pdfkit
import os

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    dato = request.form['dato']
    return f'Dato "{dato}" guardado correctamente.'

@app.route('/exportar_pdf', methods=['POST'])
def exportar_pdf():
    dato = request.form['dato']
    rendered = render_template('pdf_template.html', dato=dato)
    pdf = pdfkit.from_string(rendered, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=orden.pdf'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
