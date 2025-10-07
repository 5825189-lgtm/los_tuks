from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "tuks_secret_key"  # Necesario para usar 'session'

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

# -------------------------------
# 🧠 Crear la tabla (Flask 3.x)
# -------------------------------
with app.app_context():
    db.create_all()

# -------------------------------
# 🌐 Rutas de la aplicación
# -------------------------------

@app.route("/")
def index():
    return render_template("index.html")  # Página principal

@app.route("/menu")
def menu():
    return render_template("menu.html")  # Página del menú

@app.route("/hacer_pedido", methods=["POST"])
def hacer_pedido():
    nombre = request.form.get("nombre")
    telefono = request.form.get("telefono", "")
    pedido = request.form.get("pedido")
    total = float(request.form.get("total", 0))

    nuevo_pedido = Pedido(nombre=nombre, telefono=telefono, pedido=pedido, total=total)
    db.session.add(nuevo_pedido)
    db.session.commit()

    # Guarda los datos del pedido en sesión para mostrar en la página de gracias
    session["nombre"] = nombre
    session["total"] = total

    return redirect(url_for("gracias"))

@app.route("/gracias")
def gracias():
    nombre = session.get("nombre", "Cliente")
    total = session.get("total", 0)
    return render_template("gracias.html", nombre=nombre, total=total)

@app.route("/admin")
def admin():
    pedidos = Pedido.query.order_by(Pedido.id.desc()).all()
    return render_template("admin.html", pedidos=pedidos)

# -------------------------------
# 🚀 Ejecutar aplicación (modo local)
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
