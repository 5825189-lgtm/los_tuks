from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# -------------------------------
# 🔹 CONFIGURACIÓN DE LA BASE DE DATOS
# -------------------------------
db_config = {
    'host': os.getenv("DB_HOST", "localhost"),
    'user': os.getenv("DB_USER", "root"),
    'password': os.getenv("DB_PASSWORD", ""),
    'database': os.getenv("DB_NAME", "pupuseria")
}

db = mysql.connector.connect(**db_config)

# -------------------------------
# 🔹 RUTAS PRINCIPALES
# -------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route("/gracias", methods=["POST"])
def gracias():
    nombre = request.form["nombre"]
    telefono = request.form.get("telefono", "")
    pedido = request.form["pedido"]
    total = request.form["total"]

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO pedidos (nombre, telefono, pedido, total) VALUES (%s, %s, %s, %s)",
        (nombre, telefono, pedido, total)
    )
    db.commit()

    return render_template("gracias.html", nombre=nombre, pedido=pedido, total=total)

@app.route("/admin")
def admin():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, telefono, pedido, total, fecha FROM pedidos ORDER BY fecha DESC")
    pedidos = cursor.fetchall()

    # 🔹 Calcular total general
    cursor.execute("SELECT SUM(total) AS total_general FROM pedidos")
    total_general = cursor.fetchone()["total_general"] or 0

    cursor.close()
    return render_template("admin.html", pedidos=pedidos, total_general=total_general)


# -------------------------------
# 🔹 INICIALIZACIÓN DEL SERVIDOR
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
