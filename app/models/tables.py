from app import db, lm
from sqlalchemy.sql import func
from sqlalchemy.dialects.sqlite import BLOB

class User(db.Model):
    __tablename__ = "users"
    id_usuario = db.Column('id_usuario',db.Integer,primary_key=True)
    email = db.Column('email',db.String(255), unique=True, nullable = False)
    password = db.Column('senha',db.String(255),nullable = False)
    nome = db.Column('nome',db.String(255),nullable = False)
    sobrenome = db.Column('sobrenome',db.String(255),nullable = False)
    cep = db.Column('cep',db.String(255),nullable = False)
    estado = db.Column('estado',db.String(255),nullable = False)
    cidade = db.Column('cidade',db.String(255),nullable = False)
    bairro = db.Column('bairro',db.String(255),nullable = False)
    telefone = db.Column('telefone',db.String(255),nullable = False)

    def __init__(self,email, password, nome, sobrenome,cep, estado, cidade, bairro, telefone):
        self.email = email
        self.password = password
        self.nome = nome
        self.sobrenome = sobrenome
        self.cep = cep
        self.estado = estado
        self.cidade = cidade
        self.bairro = bairro
        self.telefone = telefone

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id_usuario)

    def __repr__(self):
        return "<User %r>" % self.email


class Post(db.Model):
    __tablename__ = "posts"
    id_post = db.Column('id_post',db.Integer,primary_key=True)
    titulo = db.Column('titulo',db.String(255),nullable = False)
    descricao = db.Column('descricao',db.String(255), nullable = False)
    img_1 = db.Column('img_1', BLOB, nullable= True)
    img_2 = db.Column('img_2', BLOB, nullable= True)
    img_3 = db.Column('img_3', BLOB, nullable= True)
    img_4 = db.Column('img_4', BLOB, nullable= True)
    data_hora = db.Column(db.DateTime(timezone=True), server_default=func.now())
    id_usuario = db.Column('id_usuario',db.Integer, db.ForeignKey('users.id_usuario'))
    id_categoria = db.Column('id_categoria',db.Integer, db.ForeignKey('categorys.id_categoria'))

    user = db.relationship('User', foreign_keys = id_usuario)
    categoria = db.relationship('Category', foreign_keys = id_categoria)

    def __init__(self,titulo, descricao, img_1,img_2,img_3,img_4):
        self.titulo= titulo
        self.descricao = descricao
        self.img_1 = img_1
        self.img_2 = img_2
        self.img_3 = img_3
        self.img_4 = img_4

    
    def __repr__(self):
        return "<Project %r>" % self.id_post
    

class Category(db.Model):
    __tablename__ = "categorys"
    id_categoria = db.Column('id_categoria', db.Integer,primary_key=True)
    nome_categoria = db.Column('nome_categoria',db.String(255),unique=True, nullable = False)

    def __init__(self, nome_categoria):
        self.nome_categoria = nome_categoria
    
    def __repr__(self):
        return "<Category %r>" % self.nome_categoria