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

# Si estás en local y no hay URL de Render, usa SQLite
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
    fecha = db.Column(db.DateTime, server_default=db.func.now())

# -------------------------------
# 🧠 Crear la tabla automáticamente
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
    nombre = request.form.get("nombre")
    telefono = request.form.get("telefono", "")
    pedido = request.form.get("pedido")
    total = request.form.get("total")

    # Validar datos antes de guardar
    if not nombre or not pedido or not total:
        return "Error: faltan datos en el formulario", 400

    try:
        total = float(total)
    except ValueError:
        total = 0.0

    nuevo_pedido = Pedido(nombre=nombre, telefono=telefono, pedido=pedido, total=total)
    db.session.add(nuevo_pedido)
    db.session.commit()

    return redirect(url_for("gracias", total=total))

@app.route("/gracias")
def gracias():
    total = request.args.get("total", 0)
    return render_template("gracias.html", total=total)

@app.route("/admin")
def admin():
    pedidos = Pedido.query.all()
    total_general = sum(p.total for p in pedidos) if pedidos else 0
    return render_template("admin.html", pedidos=pedidos, total_general=total_general)

# -------------------------------
# 🚀 Ejecutar aplicación en local
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
