#Importacion de librerias en Flask
# Flask: funciones de microframework
#render_template: permite renderizar los HTML en el servidor
from flask import Flask,redirect,url_for,render_template,request,g,session,flash
import sqlite3
import os
from flask_mail import Mail,Message
import bcrypt
currentdirectory = os.path.dirname(os.path.abspath(__file__))
DATABASE= '/home/diegoaaa/Desktop/pagina web/Proyecto_Cafeteria - copia-20201211T023939Z-001/Proyecto_Cafeteria - MAIL+BACKEND/database.db'
#Establezco el objeto Flask
app=Flask(__name__)


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


@app.route("/")
def index():
    return render_template('index.html')
@app.route("/loginAdmin")
def loginAdmin():
    return render_template('loginAdmin.html')
@app.route("/loginCajero")
def loginCajero():
    return render_template('loginCajero.html')
#Recuperacion de Contrasena
@app.route("/olvidaste")
def olvidaste():
    return render_template('RecupContra.html')


#Crear usuario
@app.route("/crearusuario",methods=['GET','POST'])
def crearusuario():
    if (request.method=="GET"):
        if 'nombre' in session:
            return render_template('index.html')
        else:
            return render_template('index.html')
    else:
        nombre = request.form['nmNombreRegistro']
        correo = request.form['nmCorreoRegistro']
        password = request.form['nmPasswordRegistro']
        password_encode = password.encode("utf-8")
        password_encriptado = bcrypt.hashpw(password_encode, semilla)

        connection = sqlite3.connect(currentdirectory+"\database.db")
        #Crea el cursor
        cursor = connection.cursor()


        #PREPARA EL QUERY PARA INSERCION
        sQuery = "INSERT into Login values(correo,password,nombre) VALUES (%s, %s, %s)"
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