import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'mipetito_secret')
app.permanent_session_lifetime = timedelta(minutes=30)

# DATABASE_URL desde entorno (Render proveerá esto)
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    db_url = "sqlite:///pedidos.db"  # fallback local para pruebas
# SQLAlchemy >=1.4 necesita "postgresql://" en vez de "postgres://"
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50))
    pedido = db.Column(db.String(300), nullable=False)
    total = db.Column(db.String(20), nullable=False)

@app.before_first_request
def crear_tablas():
    db.create_all()

# admin credentials desde entorno (mejor que estén como variables)
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASS = os.environ.get('ADMIN_PASS', '1234')

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/realizar_pedido', methods=['POST'])
def realizar_pedido():
    nombre = request.form['nombre']
    telefono = request.form.get('telefono', '')
    pedido_desc = request.form['pedido']
    total = request.form['total']
    nuevo = Pedido(nombre=nombre, telefono=telefono, pedido=pedido_desc, total=total)
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('menu'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        if usuario == ADMIN_USER and password == ADMIN_PASS:
            session['admin'] = usuario
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error="Credenciales incorrectas")
    return render_template('login.html')

@app.route('/admin')
def admin():
    if 'admin' in session:
        pedidos = Pedido.query.order_by(Pedido.id.desc()).all()
        return render_template('admin.html', pedidos=pedidos)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
