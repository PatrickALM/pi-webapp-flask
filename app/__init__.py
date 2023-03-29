# Modulo que realiza o processo de instancia do Flask e do banco de dados
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
# define as configurações necessárias do Flask a partir do modulo config
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

lm = LoginManager()
lm.init_app(app)

# Necessario importar os modulos que contem a estrutura de tabelas, formularios e rotas após a instancia do Flask
from app.models import tables, forms
from app.controllers import default
