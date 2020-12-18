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
login_manager.login_view = "loginAdmin"
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
from forms import LoginCajeroForm, LoginAdminForm
## ---------------------------------------------------------



@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None


@app.route("/")
# @app.route("/login", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/loginAdmin")
def loginAdmin():
    if current_user.is_authenticated:
        return redirect(url_for('PaginaInicial_Admin.html'))
    form = LoginAdminForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('loginAdmin')
            return redirect(next_page)
    return render_template('loginAdmin.html', form=form)


@app.route("/loginCajero", methods=['GET', 'POST'])
def loginCajero():
    if current_user.is_authenticated:
        return redirect(url_for('PaginaInicial_Cajero.html'))
    form = LoginCajeroForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('loginCajero')
            return redirect(next_page)
    return render_template('loginCajero.html', form=form)

#Recuperacion de Contrasena
@app.route("/olvidaste", methods=['GET', 'POST'])
def olvidaste():
    return render_template('RecupContra.html')


#Crear usuario
@app.route("/crearusuario",methods=['GET','POST'])
def crearusuario():
    if (request.method=="GET"):
        if 'nombre' in session:
            return render_template('index.html')
        else:
            return render_template('crearuser.html')
    else:
        nombre = request.form['nmNombreRegistro']
        #correo = request.form['nmCorreoRegistro']
        password = request.form['nmPasswordRegistro']
        password_encode = password.encode("utf-8")
        password_encriptado = bcrypt.hashpw(password_encode, semilla)

        connection = sqlite3.connect(currentdirectory+"\database.db")
        #Crea el cursor
        cursor = connection.cursor()


        #PREPARA EL QUERY PARA INSERCION
        #sQuery = "INSERT INTO Login values('{n}',{email},{pwd})".format(n = nombre, email=correo, pwd=password)
        sQuery = "INSERT INTO login1 values('{n}',{pwd})".format(n = nombre, pwd=password)
        # Ejecuta la sentencia
        cursor.execute(sQuery)

        # Ejectura el Commit
        connection.commit()

        ##Registra la sesion

        session['nombre'] = nombre
        #session['correo'] = correo

        return redirect(url_for('index'))
  



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
def paginaPrinAdmin():
    return render_template('PaginaInicial_Admin.html')

##PAGINA PRINCIPAL CAJEROS

@app.route("/paginaPrinCajero",methods=['GET','POST'])
def paginaPrinCajero():
    return render_template('PaginaInicial_Cajero.html')

#Gestion de Cajeros
@app.route('/gescajeros',methods=['GET','POST'])
def gescajero():
    return render_template('GestionCajeros.html')
#genere otra ruta para Actualizar-Eliminar Cajeros desde GESTIONCAJEROS #D3A
@app.route("/actuEliCajero",methods=['GET','POST'])
def actuEliCajero():
    return render_template('ActElimCajeros.html')

#Registro de Productos
@app.route('/regisproducto',methods=['GET','POST'])
def regisproducto():
    return render_template('CrearProducto.html')

#Crear Productos
@app.route('/crearproducto',methods=['GET','POST'])
def crearproducto():
    return render_template('CrearProducto.html')

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

if __name__ == '__main__':
    #Lanzar el servidor
    app.run(port=5000,debug=True)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
