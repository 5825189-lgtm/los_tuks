from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# -------------------------------
# 🔧 Configuración de la Base de Datos
# -------------------------------
db_url = os.environ.get("DATABASE_URL")  # Render usará esta variable automáticamente
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Si estás en local, usa SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///pedidos_local.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -------------------------------
# 🧾 Modelo de la tabla Pedidos
# -------------------------------
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    pupusa = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)

# -------------------------------
# 🧠 Crear la tabla si no existe
# -------------------------------
with app.app_context():
    db.create_all()

# -------------------------------
# 🌐 Rutas de la aplicación
# -------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/hacer_pedido", methods=["POST"])
def hacer_pedido():
    nombre = request.form["nombre"]
    pupusa = request.form["pupusa"]
    cantidad = int(request.form["cantidad"])

    # 💵 Precios según tipo de pupusa
    precios = {
        "Frijol con queso": 0.35,
        "Revueltas": 0.35,
        "Especialidad de la casa": 0.60
    }

    total = precios.get(pupusa, 0) * cantidad

    nuevo_pedido = Pedido(nombre=nombre, pupusa=pupusa, cantidad=cantidad, total=total)
    db.session.add(nuevo_pedido)
    db.session.commit()

    return render_template("gracias.html", total=total)

@app.route("/gracias")
def gracias():
    return render_template("gracias.html", total=0)

@app.route("/admin")
def admin():
    pedidos = Pedido.query.all()
    total_general = sum(p.total for p in pedidos)
    return render_template("admin.html", pedidos=pedidos, total_general=total_general)

# -------------------------------
# 🚀 Ejecutar en local
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
