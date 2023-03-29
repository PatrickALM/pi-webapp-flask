from app import db, lm

class User(db.Model):
    __tablename__ = "users"
    id_usuario = db.Column('id_usuario',db.Integer,primary_key=True)
    nome_usuario = db.Column('nome_usuario',db.String(255),unique=True, nullable = False)
    password = db.Column('senha',db.String(255),nullable = False)
    nome = db.Column('nome',db.String(255),nullable = False)
    sobrenome = db.Column('sobrenome',db.String(255),nullable = False)
    email = db.Column('email',db.String(255), unique=True, nullable = False)
    cep = db.Column('cep',db.String(255),nullable = False)
    estado = db.Column('estado',db.String(255),nullable = False)
    cidade = db.Column('cidade',db.String(255),nullable = False)
    bairro = db.Column('bairro',db.String(255),nullable = False)
    telefone = db.Column('telefone',db.String(255),nullable = False)

    def __init__(self,nome_usuario, password, nome, sobrenome, email, cep, estado, cidade, bairro, telefone):
        self.nome_usuario = nome_usuario
        self.password = password
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
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
        return "<User %r>" % self.nome_usuario


class Post(db.Model):
    __tablename__ = "posts"
    id_post = db.Column('id_post',db.Integer,primary_key=True)
    titulo = db.Column('titulo',db.String(255),nullable = False)
    descricao = db.Column('descricao',db.String(255))
    #data_hora = db.Column('data_hora', db.Datetime)
    #img_1 = db.Column('img_1', db.Blob)
    #img_2 = db.Column('img_2', db.Blob)
    #img_3 = db.Column('img_3', db.Blob)
    #img_4 = db.Column('img_4', db.Blob)
    id_usuario = db.Column('id_usuario',db.Integer, db.ForeignKey('users.id_usuario'))
    id_categoria = db.Column('id_categoria',db.Integer, db.ForeignKey('categorys.id_categoria'))

    user = db.relationship('User', foreign_keys = id_usuario)
    categoria = db.relationship('Category', foreign_keys = id_categoria)

    def __init__(self,title, description, id_user):
        self.title= title
        self.description = description
        self.id_user = id_user
    
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