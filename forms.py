from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_wtf.file import FileField, FileRequired
from email_validator import validate_email, EmailNotValidError


class NumberValidator(ValueError):
    def __init__(self, message='', *args, **kwargs):
        ValueError.__init__(self, message, *args, **kwargs)
    def __call__(self, form, field):
        try:
            data = field.data
            int(data)
        except ValueError as ve:
            return ValidationError(ve.__str__())


class EmailValidator(EmailNotValidError):
    def __init__(self, *args, **kwargs):
        EmailNotValidError.__init__(self, *args, **kwargs)
    def __call__(self, form, field):
        try:
            data = field.data
            validate_email(data)
        except EmailNotValidError as enve:
            return ValidationError(enve.__str__())


class LoginAdminForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')


class LoginCajeroForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')


class RegistroCajeroForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=64)])
    cedula = StringField('Cedula', validators=[DataRequired(), NumberValidator()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password_check = PasswordField('Repeat Password', validators=[DataRequired(),Length(min=8)])
    email = StringField('Email', validators=[EmailValidator()])
    submit = SubmitField('Login')


class AgregarProducto(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    description = TextAreaField('Descripcion', validators=[DataRequired()])
    image = FileField('Imagen', validators=[FileRequired()])
    quantity = FileField('') 


