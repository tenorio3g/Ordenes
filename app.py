from flask import Flask, render_template, request, redirect, send_file
import sqlite3, csv

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("base.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS ordenes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        area TEXT, trabajo TEXT, celda TEXT, requisitor TEXT, planta TEXT, supervisor TEXT,
        fecha_requisicion TEXT, numero_orden TEXT
    )""")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def formulario():
    if request.method == "POST":
        datos = request.form
        conn = sqlite3.connect("base.db")
        c = conn.cursor()
        c.execute("""INSERT INTO ordenes (area, trabajo, celda, requisitor, planta, supervisor,
            fecha_requisicion, numero_orden) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datos.get("area"), datos.get("trabajo"), datos.get("celda"),
            datos.get("requisitor"), datos.get("planta"), datos.get("supervisor"),
            datos.get("fecha_requisicion"), datos.get("numero_orden")
        ))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("formulario.html")

@app.route("/exportar")
def exportar():
    conn = sqlite3.connect("base.db")
    c = conn.cursor()
    c.execute("SELECT * FROM ordenes")
    filas = c.fetchall()
    conn.close()
    with open("ordenes_exportadas.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Área", "Trabajo", "Celda", "Requisitor", "Planta", "Supervisor", "Fecha Req.", "N° Orden"])
        writer.writerows(filas)
    return send_file("ordenes_exportadas.csv", as_attachment=True)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
