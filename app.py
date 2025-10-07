from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Conexión a la base de datos (Render)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///pedidos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de tabla
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    tipo_pupusa = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

# Crear la tabla (solo la primera vez)
with app.app_context():
    db.create_all()

# Página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Menú con formulario
@app.route('/menu')
def menu():
    return render_template('menu.html')

# Guardar pedido
@app.route('/hacer_pedido', methods=['POST'])
def hacer_pedido():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    tipo_pupusa = request.form['tipo_pupusa']
    cantidad = int(request.form['cantidad'])

    nuevo_pedido = Pedido(
        nombre=nombre,
        telefono=telefono,
        direccion=direccion,
        tipo_pupusa=tipo_pupusa,
        cantidad=cantidad
    )
    db.session.add(nuevo_pedido)
    db.session.commit()

    return redirect('/gracias')

# Página de agradecimiento
@app.route('/gracias')
def gracias():
    return render_template('gracias.html')

# Panel de administración
@app.route('/admin')
def admin():
    pedidos = Pedido.query.all()
    return render_template('admin.html', pedidos=pedidos)

if __name__ == '__main__':
    app.run(debug=True)
