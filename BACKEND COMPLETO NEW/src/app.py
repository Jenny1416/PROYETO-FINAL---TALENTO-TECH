import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = '1234'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Función para obtener el precio de un producto
def obtener_precio(producto):
    precios = {
        'camiseta': 20.0,
        'pantalones': 40.0,
        'zapatos': 60.0
    }
    return precios.get(producto, 0.0)

def get_all_products():
    return Producto.query.all()

# Clases Usadas
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto = db.Column(db.String(120), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.relationship('Usuario', backref=db.backref('pedidos', lazy=True))

class Carrito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    producto = db.Column(db.String(120), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('carrito', lazy=True))

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.String(250))

# Rutas
@app.route('/')
def home():
    if 'usuario_id' in session:
        return redirect(url_for('perfil'))
    return render_template('home.html')

@app.route('/perfil')
def perfil():
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
        return render_template('perfil.html', usuario=usuario)
    else:
        return redirect(url_for('login'))

@app.route('/actualizar_perfil', methods=['GET', 'POST'])
def actualizar_perfil():
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
        if request.method == 'POST':
            usuario.nombre = request.form['nombre']
            usuario.email = request.form['email']
            db.session.commit()
            return redirect(url_for('perfil'))
        return render_template('actualizar_perfil.html', usuario=usuario)
    else:
        return redirect(url_for('login'))

@app.route('/historial_pedidos')
def historial_pedidos():
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
        return render_template('historial_pedidos.html', pedidos=usuario.pedidos)
    else:
        return redirect(url_for('login'))

@app.route('/productos')
def productos():
    productos = get_all_products()  # Esta función debería devolver una lista de productos desde la base de datos
    return render_template('productos.html', productos=productos)

@app.route('/pedidos')
def pedidos():
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
        return render_template('pedidos.html', pedidos=usuario.pedidos)
    else:
        return redirect(url_for('login'))
    
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            email = request.form['email']
            contraseña = generate_password_hash(request.form['contraseña'])
            nuevo_usuario = Usuario(nombre=nombre, email=email, contraseña=contraseña)
            db.session.add(nuevo_usuario)
            db.session.commit()
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            return f"Error al registrar el usuario: {e}"
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
        if usuario.is_admin:
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('perfil'))
    
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['contraseña']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.contraseña, contraseña):
            session['usuario_id'] = usuario.id
            if usuario.is_admin:
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('perfil'))
        else:
            return 'Credenciales incorrectas, por favor intenta de nuevo.'
    return render_template('login.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Aquí puedes implementar la lógica para enviar un correo de recuperación de contraseña
        return 'Instrucciones enviadas a tu correo electrónico.'
    return render_template('forgot_password.html')


@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('home'))

@app.before_request
def crear_admin():
    if not Usuario.query.filter_by(email="admin@example.com").first():
        nombre = "Admin"
        email = "admin@example.com"
        contraseña = generate_password_hash("adminpassword")
        admin = Usuario(nombre=nombre, email=email, contraseña=contraseña, is_admin=True)
        
        db.session.add(admin)
        db.session.commit()
        print("Cuenta de administrador creada con éxito")

@app.route('/admin')
def admin():
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
        if usuario.is_admin:
            productos = Producto.query.all()
            return render_template('admin.html', productos=productos)
        else:
            return 'Acceso denegado'
    else:
        return redirect(url_for('login'))   

@app.route('/admin/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
        if usuario.is_admin:
            if request.method == 'POST':
                nombre = request.form['nombre']
                precio = request.form['precio']
                descripcion = request.form['descripcion']
                nuevo_producto = Producto(nombre=nombre, precio=precio, descripcion=descripcion)
                db.session.add(nuevo_producto)
                db.session.commit()
                return redirect(url_for('admin'))
            return render_template('agregar_producto.html')
        else:
            return 'Acceso denegado'
    else:
        return redirect(url_for('login'))     

@app.route('/admin/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
        if usuario.is_admin:
            producto = Producto.query.get(id)
            if request.method == 'POST':
                producto.nombre = request.form['nombre']
                producto.precio = request.form['precio']
                producto.descripcion = request.form['descripcion']
                db.session.commit()
                return redirect(url_for('admin'))
            return render_template('editar_producto.html', producto=producto)
        else:
            return 'Acceso denegado'
    else:
        return redirect(url_for('login'))

@app.route('/admin/eliminar_producto/<int:id>')
def eliminar_producto(id):
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
        if usuario.is_admin:
            producto = Producto.query.get(id)
            db.session.delete(producto)
            db.session.commit()
            return redirect(url_for('admin'))
        else:
            return 'Acceso denegado'
    else:
        return redirect(url_for('login'))               

@app.route('/carrito')
def ver_carrito():
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
        return render_template('carrito.html', carrito=usuario.carrito)
    else:
        return redirect(url_for('login'))

@app.route('/agregar_al_carrito/<producto>', methods=['POST'])
def agregar_al_carrito(producto):
    if 'usuario_id' in session:
        usuario_id = session['usuario_id']
        cantidad = request.form['cantidad']
        nuevo_item = Carrito(usuario_id=usuario_id, producto=producto, cantidad=cantidad)
        db.session.add(nuevo_item)
        db.session.commit()
        return redirect(url_for('ver_carrito'))
    else:
        return redirect(url_for('login'))

@app.route('/eliminar_del_carrito/<int:id>')
def eliminar_del_carrito(id):
    if 'usuario_id' in session:
        item = Carrito.query.get(id)
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('ver_carrito'))
    else:
        return redirect(url_for('login'))

@app.route('/procesar_pago', methods=['POST'])
def procesar_pago():
    if 'usuario_id' in session:
        usuario = Usuario.query.get(session['usuario_id'])
        total = sum(item.cantidad * obtener_precio(item.producto) for item in usuario.carrito)
        # Aquí simulamos el pago
        session['pago_exitoso'] = True
        # Crear registros de pedidos y vaciar el carrito
        for item in usuario.carrito:
            nuevo_pedido = Pedido(usuario_id=usuario.id, producto=item.producto, cantidad=item.cantidad)
            db.session.add(nuevo_pedido)
            db.session.delete(item)
        db.session.commit()
        return redirect(url_for('confirmacion_pago'))
    else:
        return redirect(url_for('login'))

@app.route('/confirmacion_pago')
def confirmacion_pago():
    if 'pago_exitoso' in session:
        session.pop('pago_exitoso', None)
        return render_template('confirmacion_pago.html')
    else:
        return redirect(url_for('home'))

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'  # Esto es opcional, ya que Flask usa 'static' por defecto


# Inicio de la aplicación
if __name__ == '__main__':
    app.run(debug=True)