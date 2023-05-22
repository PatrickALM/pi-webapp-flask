import os.path
basedir = os.path.abspath(os.path.dirname(__file__))


### CONEXÃO COM MYSQL ###
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:J2*5TSuBHQ8M@localhost/prototipo_pi23'



### CONEXÃO COM SQLITE ###
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir,'storage.db')
SECRET_KEY = "SENHA_BEM_SEGURA"


UPLOAD_FOLDER = "./app/static/images/upload_img"
ALLOWED_EXTENSIONS = ['png','jpg','jpeg']


