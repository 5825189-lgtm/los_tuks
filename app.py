from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# -------------------------------
# 🔧 Configuración de la Base de Datos
# -------------------------------
db_url = os.environ.get("DATABASE_URL")  # Render usará esta variable automáticamente

# 🔄 Ajuste necesario para Render (Postgres)
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Base local si no hay base en línea
app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///pedidos_local.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------------------
# 🧾 Modelo de la tabla Pedidos
# -------------------------------
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    pedido = db.Column(db.Text, nullable=False)
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())

# -------------------------------
# 🧠 Crear la tabla (Flask 3.x compatible)
# -------------------------------
with app.app_context():
    db.create_all()

# -------------------------------
# 🌐 Rutas principales
# -------------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/hacer_pedido", methods=["POST"])
def hacer_pedido():
    try:
        nombre = request.form["nombre"]
        telefono = request.form.get("telefono", "")
        pedido = request.form["pedido"]
        total = request.form["total"]

        nuevo_pedido = Pedido(nombre=nombre, telefono=telefono, pedido=pedido, total=float(total))
        db.session.add(nuevo_pedido)
        db.session.commit()

        return render_template("gracias.html", total=total)
    except Exception as e:
        print("❌ Error al procesar pedido:", e)
        return "Error al procesar el pedido", 400

@app.route("/gracias")
def gracias():
    return render_template("gracias.html")

@app.route("/admin")
def admin():
    pedidos = Pedido.query.order_by(Pedido.fecha.desc()).all()
    total_general = sum(p.total for p in pedidos)
    return render_template("admin.html", pedidos=pedidos, total_general=total_general)

# -------------------------------
# 🚀 Ejecutar aplicación (modo local)
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
