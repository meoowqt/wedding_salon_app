from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, TextAreaField, DateTimeField, HiddenField
from wtforms.validators import DataRequired, Email
from wtforms.validators import EqualTo, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])

class ProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    price = FloatField('Цена', validators=[DataRequired()])
    description = TextAreaField('Описание')

class AppointmentForm(FlaskForm):
    cart_item_id = HiddenField(validators=[DataRequired()])
    date = DateTimeField('Дата примерки', format='YYYY-MM-DD', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Повтор пароля', 
                              validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
