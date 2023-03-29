'''
Este módulo é responsável por fazer o controle de quais rotas podem ser utilizadas
para acessar as páginas, os templates que devem ser renderizados e interações com
formulários
'''
from app import app, db, lm
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user

from app.models.tables import User, Post, Category
from app.models.forms import LoginForm


@lm.user_loader
def load_user(id_usuario):
    return User.query.filter_by(id_usuario=id_usuario).first()

@app.route("/index")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(nome_usuario=form.username.data).first()
        if u and u.password == form.password.data:
            login_user(u)
            flash("Usuário Logado")
            return redirect(url_for("index"))
        else:
            flash("Login Inválido")
    else:
        print(form.errors)
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash("Usuario deslogado")
    return redirect(url_for("index"))


@app.route("/register")
def register():
    return "Formulário de cadastro"

@app.route("/doacoes")
def doacoes():
    return "Pagina com filtros para o usuário visualizar todos os itens que estão sendo doados no momento"

@app.route("/sobre")
def sobre():
    return "Pagina para descrever projeto da Univesp e integrantes "

#@app.route("/doacoes/<int: id>")
#def pg_item():
#    return "pagina template para cada item sendo doado no site"

@app.route("/profile")
def profile():
    return "pagina de perfil de usuario"



#pagina de teste para inserir dados no banco (CREATE)
@app.route("/teste/<info>")
@app.route("/teste", defaults={"info": None})
def teste(info):
    i = User("palmeida", "123", "patrick", "almeida", "patrick@gmail.com", "125361253", "Sao Paulo", "Sao Paulo",
              "Cidade Tiradentes","88888516428")
    db.session.add(i)
    db.session.commit()
    return "Usuario registrado"

#pagina de teste para selecionar dados no banco (READ)
@app.route("/teste2/<info>")
@app.route("/teste2", defaults={"info": None})
def teste2(info):
    r= User.query.filter_by(estado= "Sao Paulo").all()
    print(r)
    return "Ok"

#pagina de teste para atualizar dados no banco (UPDATE)
@app.route("/teste3/<info>")
@app.route("/teste3", defaults={"info": None})
def teste3(info):
    r= User.query.filter_by(estado= "Sao Paulo").first()
    r.nome = "Patrick"
    db.session.add(r)
    db.session.commit()
    return "Registro Atualizado"


