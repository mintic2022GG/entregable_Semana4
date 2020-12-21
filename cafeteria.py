#Importacion de librerias en Flask
# Flask: funciones de microframework
#render_template: permite renderizar los HTML en el servidor

# bibliotecas nativas de python 
import os
import sqlite3

# flask
from flask import Flask,redirect,url_for,render_template,request,g,session,flash

# paquetes para enviar mensajes al correo 
from flask_mail import Mail,Message

# manejo de SQL
from flask_sqlalchemy import SQLAlchemy

# manejo de las sesiones
from flask_login import LoginManager, logout_user, current_user, login_user, login_required


from werkzeug.urls import url_parse

import bcrypt

currentdirectory = os.path.dirname(os.path.abspath(__file__))

# TODO:Use a relative path
DATABASE_PATH = 'sqlite:///cafeteria.db'

#Establezco el objeto Flask
# esta es la aplicaicon principal
app=Flask(__name__)     

# ----------------------------------------------------------------------------
# gestor de la base de datos
# ----------------------------------------------------------------------------
# configuracion para el acceso a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# se crea gestor de base de datos que permite el acceso, modificacion de la base
# de datos
db = SQLAlchemy(app)
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# manejo de las sesiones
# ----------------------------------------------------------------------------
login_manager = LoginManager(app)
# en caso que se intente acceder a una pagina restringida se renderiza esta pagina
login_manager.login_view = "index" 
# ----------------------------------------------------------------------------


##este el codigo para el envio del correo
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'correo@gmail.com'
app.config['MAIL_PASSWORD'] = 'contrasenade correo'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
##---------------------------------------------------------#

##Creo llave secreta
app.secret_key="appLogin"
## Creo semilla
semilla = bcrypt.gensalt()

## ---------------------------------------------------------
# llamamos los models
# ---------------------------------------------------------#
from models import *
# ---------------------------------------------------------#

## ---------------------------------------------------------
# llamamos los formularios para login, registros y agregar
# productos
# ---------------------------------------------------------#
from forms import LoginCajeroForm, LoginAdminForm, RegistroCajeroForm, AgregarProducto
## ---------------------------------------------------------

# obtiene el usuario de la base de datos
@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/logout')
def logout():
    logout_user()
    # return "Sesion finalizada con exito"
    return redirect(url_for('index'))

@app.route("/")
# @app.route("/login", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/loginAdmin", methods=['GET', 'POST'])
def loginAdmin():
    if current_user.is_authenticated:
        return redirect(url_for('paginaPrinAdmin'))
    form = LoginAdminForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        only_admin = user.type_user == 'admin'
        if user is not None and user.check_password(form.password.data) and only_admin:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('paginaPrinAdmin')
            return redirect(next_page)
    return render_template('loginAdmin.html', form=form)


@app.route("/loginCajero", methods=['GET', 'POST'])
def loginCajero():
    if current_user.is_authenticated:
        return redirect(url_for('paginaPrinCajero'))
    form = LoginCajeroForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('paginaPrinCajero')
            return redirect(next_page)
    return render_template('loginCajero.html', form=form)

#Recuperacion de Contrasena
@app.route("/olvidaste", methods=['GET', 'POST'])
def olvidaste():
    return render_template('RecupContra.html')


#Crear usuario
@app.route("/crearusuario",methods=['GET','POST'])
@login_required
def crearusuario():
    form = RegistroCajeroForm()
    error = None
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        password = form.password.data
        password_check = form.password_check.data
        cedula = form.cedula.data
        check_email = User.get_by_email(email=email)
        check_username = User.get_by_username(username=name)
        check_cedula = User.get_by_cedula(cedula=cedula)
        if check_email is not None:
            error = f'El email "{email}" ya está siendo utilizado por otro usuario'
        elif check_username is not None:
            error = f'El username "{name}" ya está siendo utilizado por otro usuario'
        elif check_cedula is not None:
            error = f'la cedula "{cedula}" ya está siendo utilizado por otro usuario'
        elif password_check != password_check:
            error = f'Las contraseñas no coinciden'
        else:
            cajero = User()
            cajero.email = email
            cajero.username = name
            cajero.type_user = 'cajero'
            cajero.set_password(password)
            cajero.save()
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('paginaPrinAdmin')
            return redirect(next_page)
    return render_template('crearuser.html', form=form)


@app.route('/send_password',methods=['GET','POST'])
def send_password():
    if request.method == "POST":
        email=request.form['email']
        subject= 'Recuperacion contrasena usuario'
        msg = 'Usted ha solicitado la recuperacion de la contrasena que es #1231234'
        message = Message(subject,sender='correo@gmail.com',recipients=[email])
        message.body = msg

        mail.send(message)
    return render_template('result.html')

##PAGINA PRINCIPAL DE ADMIN 
@app.route("/paginaPrinAdmin",methods=['GET','POST'])
@login_required
def paginaPrinAdmin():
    return render_template('PaginaInicial_Admin.html')

##PAGINA PRINCIPAL CAJEROS

@app.route("/paginaPrinCajero",methods=['GET','POST'])
def paginaPrinCajero():
    return render_template('PaginaInicial_Cajero.html')

#Gestion de Cajeros
@app.route('/gescajeros',methods=['GET','POST'])
@login_required
def gescajero():
    form = RegistroCajeroForm()
    error = None
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data
        password = form.password.data
        password_check = form.password_check.data
        cedula = form.cedula.data
        check_email = User.get_by_email(email=email)
        check_username = User.get_by_username(username=name)
        check_cedula = User.get_by_cedula(cedula=cedula)
        if check_email is not None:
            error = f'El email "{email}" ya está siendo utilizado por otro usuario'
        elif check_username is not None:
            error = f'El username "{name}" ya está siendo utilizado por otro usuario'
        elif check_cedula is not None:
            error = f'la cedula "{cedula}" ya está siendo utilizado por otro usuario'
        elif password_check != password_check:
            error = f'Las contraseñas no coinciden'
        else:
            cajero = User(username=name, email=email, cedula=cedula, type_user='cajero')
            cajero.set_password(password)
            cajero.save()
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('paginaPrinAdmin')
            return redirect(next_page)
    return render_template('GestionCajeros.html', form=form)


#genere otra ruta para Actualizar-Eliminar Cajeros desde GESTIONCAJEROS #D3A
@app.route("/actuEliCajero",methods=['GET','POST'])
def actuEliCajero():
    return render_template('ActElimCajeros.html')

#Registro de Productos
@app.route('/regisproducto',methods=['GET','POST'])
@login_required
def regisproducto():
    form = AgregarProducto()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        quantity = int(form.quantity.data)
        price = float(form.price.data)
        producto = Product.get_by_name(name)
        if producto is not None:
            error = f'ya existe un producto con este nombre'
        else:
            p = Product(name=name, description=description, quantity=quantity, price=price)
            p.save()
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('paginaPrinCajero')
            return redirect(next_page)
    return render_template('CrearProducto.html', form=form)

#Crear Productos
@app.route('/crearproducto',methods=['GET','POST'])
@login_required
def crearproducto():
    form = AgregarProducto()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        quantity = int(form.quantity.data)
        price = float(form.price.data)
        producto = Product.get_by_name(name)
        if producto is not None:
            error = f'ya existe un producto con este nombre'
        else:
            p = Product(name=name, description=description, quantity=quantity, price=price)
            p.save()
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('paginaPrinCajero')
            return redirect(next_page)
    return render_template('CrearProducto.html', form=form)

#Actualizar y Eliminar Producto
@app.route('/actelimproducto',methods=['GET','POST'])
def actelimproducto():
    return render_template('ActualizarEliminarProducto.html')

#Gestion de Ventas
@app.route('/gestionventas',methods=['GET','POST'])
def gestionventas():
    return render_template('GestionDeVentas.html')

#Buscar Producto
@app.route('/buscarproducto',methods=['GET','POST'])
def buscarproducto():
    return render_template('Buscar.html')

@app.route('/listaProductos', methods=['GET', 'POST'])
@login_required
def listaProductos():
    return "lista productos"


@app.route('/listaCajeros',methods=['GET','POST'])
@login_required
def listaCajeros():
    empleados = [ item for item in User.query.all() if item.type_user != 'admin']
    print(empleados)
    return render_template('listaCajeros.html', employees=empleados)


@app.route('/deleteuser/<int:id>',methods=['GET','POST'])
@login_required
def delete_user():
    user = User.get_by_id(id)
    user.delete()
    return redirect(url_for('listaCajeros'))


if __name__ == '__main__':
    #Lanzar el servidor
    app.run(port=5000,debug=True)

