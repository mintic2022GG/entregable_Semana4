from datetime import datetime

from flask_login import UserMixin

# ----------------------------------------------------------------------
# estos paquetes permiten que se almacen de forma segura las contrasenias
# agregan salt y hacen una encriptacion hash y tambien permiten
# comprobar si las contrasenias ingresadas son correctas
# mas informacion aqui: https://techmonger.github.io/4/secure-passwords-werkzeug/ 
# ----------------------------------------------------------------------
from werkzeug.security import generate_password_hash, check_password_hash
# ----------------------------------------------------------------------


from cafeteria import db


users = []

def get_user(email):
    for user in users:
        if user.email == email:
            return user
    return None


class User(db.Model, UserMixin):
    """[summary]

    Args:
        db ([type]): [description]
        UserMixin ([type]): [description]

    Returns:
        [type]: [description]
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cedula = db.Column(db.String(80), unique=True, nullable=False)
    type_user = db.Column(db.String(80), unique=False, nullable=False) # cajero o admin
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        """[summary]

        Args:
            password ([type]): [description]
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """[summary]

        Args:
            password ([type]): [description]

        Returns:
            [type]: [description]
        """
        return check_password_hash(self.password, password)

    def save(self):
        """ save object inside database,
        this funcion is able to update data from a user row, or create it if it is necesary
        """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(_id):
        """[summary]

        Args:
            id ([type]): [description]

        Returns:
            [type]: [description]
        """
        return User.query.get(_id)
    
    @staticmethod
    def get_all():
        return User.query.get()

    @staticmethod
    def get_by_email(email):
        """[summary]

        Args:
            email ([type]): [description]

        Returns:
            [type]: [description]
        """
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_cedula(cedula):
        """[summary]

        Args:
            email ([type]): [description]

        Returns:
            [type]: [description]
        """
        return User.query.filter_by(cedula=cedula).first()

    @staticmethod
    def get_by_username(username):
        """[summary]

        Args:
            email ([type]): [description]

        Returns:
            [type]: [description]
        """
        return User.query.filter_by(username=username).first()


class Product(db.Model):
    """[summary]

    Args:
        db ([type]): [description]
    """

    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    # path_image = db.Column(db.String(256), unique=True, nullable=True)

    def __repr__(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return "Bill {}".format(self.id)

    @staticmethod
    def get_by_name(name):
        return Product.query.filter_by(name=name).first()

    def save(self):
        """ save object inside database,
        this funcion is able to update data from a user row, or create it if it is necesary
        """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Product.query.get()


class Bill(db.Model):
    """[summary]

    Args:
        db ([type]): [description]

    Returns:
        [type]: [description]
    """

    __tablename__ = 'bills'

    id = db.Column(db.Integer, primary_key=True)
    datetime_facture = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cashier_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    customer_name = db.Column(db.String(80), unique=True, nullable=False)
    customer_cedula = db.Column(db.String(80), unique=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product_price = db.Column(db.Numeric, db.ForeignKey('products.price'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # relationship
    # user = db.relationship('User', backref=db.backref('bills', lazy=True))
    # product = db.relationship('Product', backref=db.backref('bills', lazy=True))

    def __repr__(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return "Biil {}".format(self.id)

    def save(self):
        """ save object inside database,
        this funcion is able to update data from a user row, or create it if it is necesary
        """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bill.query.get()