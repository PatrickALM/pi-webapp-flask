from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")


class RegisterForm(FlaskForm):
    name = StringField("username", validators=[DataRequired()])
    last_name = StringField("last_name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(),Email()])
    phone_number = StringField("phone_number", validators=[DataRequired(), Length(min=11,max=11)])
    password = PasswordField("password", validators=[DataRequired()])
    password_auth = PasswordField("password_auth", validators=[DataRequired()])
    cep = StringField("cep", validators=[DataRequired(), Length(min=8,max=8)])
    estado = StringField("estado", validators=[DataRequired()])
    cidade = StringField("cidade", validators=[DataRequired()])
    bairro = StringField("bairro", validators=[DataRequired()])
