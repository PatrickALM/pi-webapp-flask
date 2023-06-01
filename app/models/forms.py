from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField ,SelectField,IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length,ValidationError
from wtforms_alchemy import QuerySelectField

class LoginForm(FlaskForm):
    email = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


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


class SearchForm(FlaskForm):
    busca = StringField("busca", validators=[DataRequired(),Length(max=30)])

class FilterCategory(FlaskForm):
    categorias = SelectField(u'Categorias', choices=['Todas','Bicicleta','Brinquedos','Cobertores','Eletroeletronicos','Livros','Moveis','Roupas','Sapatos'])

    
class FilterState(FlaskForm):
    estado = SelectField(u'Estado', choices=['Todos','Acre','Alagoas','Amapá','Amazonas','Bahia','Ceará','Distrito Federal','Esprírito Santo', 
                                             'Goiás', 'Maranhão','Mato Grosso','Mato Grosso do Sul', 'Minas Gerais',
                                             'Pará', 'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro','Rio Grande do Norte',
                                             'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantis'
                                             ])

class FilterOptions(FlaskForm):
    opcoes = SelectField(u'Opcoes', choices=['Mais Recentes','Mais Antigos','A-z','Z-a'])


class PostForm(FlaskForm):
    titulo = StringField("titulo", validators=[DataRequired()])
    descricao = TextAreaField("descricao", validators=[DataRequired()])
    img_1 = FileField('image')
    categorias = SelectField(u'Categorias', choices=[(1,'Bicicleta'),(2,'Brinquedos'),(3,'Cobertores'),(4,'Eletroeletronicos'),
                                                     (5,'Livros'),(6,'Moveis'),(7,'Roupas'),(8,'Sapatos')])
    

class UserEditForm(FlaskForm):
    name = StringField("username", validators=[DataRequired()])
    last_name = StringField("last_name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(),Email()])
    phone_number = StringField("phone_number", validators=[DataRequired(), Length(min=11,max=11)])
    cep = StringField("cep", validators=[DataRequired(), Length(min=8,max=8)])
    estado = SelectField('estado', choices=['Selecione o estado','Acre','Alagoas','Amapá','Amazonas','Bahia','Ceará','Distrito Federal','Esprírito Santo', 
                                             'Goiás', 'Maranhão','Mato Grosso','Mato Grosso do Sul', 'Minas Gerais',
                                             'Pará', 'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro','Rio Grande do Norte',
                                             'Rio Grande do Sul', 'Rondônia', 'Roraima', 'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantis'
                                             ])
    cidade = StringField("cidade", validators=[DataRequired()])
    bairro = StringField("bairro", validators=[DataRequired()])

    def validate_estado(form,field):
        if field.data == 'Selecione o estado':
            raise ValidationError("Selecione uma opção válida")
        
        




   


    

