'''
Este módulo é responsável por fazer o controle de quais rotas podem ser utilizadas
para acessar as páginas, os templates que devem ser renderizados e interações com
formulários
'''
from app import app, db, lm
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user

from app.models.tables import User, Post, Category
from app.models.forms import LoginForm, RegisterForm, SearchForm, FilterCategory,FilterOptions, FilterState,PostForm,UserEditForm

import base64



'''
Inicializa variáveis globais
'''
st_categoria = ""
st_estado = ""
st_opcoes = "Mais Recentes"



'''
Carrega o Load Manager, que é responsável pelo gerenciamento de sessão de usuário
'''
@lm.user_loader
def load_user(id_usuario):
    return User.query.filter_by(id_usuario=id_usuario).first()




'''
Página Principal
'''
@app.route("/index",methods=["GET","POST"])
@app.route("/",methods=["GET","POST"])
def index():
    form_register = RegisterForm()
    if form_register.validate_on_submit():
        if form_register.password.data == form_register.password_auth.data:
            u = User(form_register.email.data, form_register.password.data, form_register.name.data, form_register.last_name.data, 
                     form_register.cep.data, form_register.estado.data, form_register.cidade.data,
                     form_register.bairro.data, form_register.phone_number.data)
            db.session.add(u)
            db.session.commit()
            return redirect(url_for("register"))
        else:
            flash("Erro de confirmação de senha.")
    else:
        flash(form_register.errors)
    return render_template("index.html", form=form_register)



'''
Página de Login
'''
@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u and u.password == form.password.data:
            login_user(u)
            flash("Usuário Logado")
            return redirect(url_for("index"))
        else:
            flash("Login Inválido")
    else:
        flash(form.errors)
    return render_template("login.html", form=form)



'''
Página de busca de todos os itens cadastrados, com filtros por palavra-chave, seleção de categoria, 
seleção de estado, e seleção do tipo de ordenação que os itens serão mostrados.
'''
@app.route("/busca", methods=["GET","POST"])
def busca():
    global st_categoria 
    global st_estado
    global st_opcoes
    ordem = Post.data_hora.desc()
    form = SearchForm()
    slc_category = FilterCategory(categorias=st_categoria)
    slc_state = FilterState(estado=st_estado)
    slc_options = FilterOptions(opcoes=st_opcoes)
    

    all_data = loadData()
    

    
       
    if slc_category.data and slc_category.validate():
        st_categoria = slc_category.data['categorias']
        if slc_category.data['categorias'] != "Todas":
            all_data = []
            all_data = loadData(categoria=st_categoria,estado=st_estado, ordem=ordem)
            
        
        else:
            all_data = []
            all_data = loadData(estado=st_estado, ordem=ordem)
     
    else:
         flash(slc_category.errors)




    if slc_state.data and slc_state.validate():
        st_estado = slc_state.data['estado']
        if slc_state.data['estado'] != "Todos":
            all_data = []
            all_data = loadData(categoria=st_categoria,estado=st_estado, ordem=ordem)
        
        else:
            all_data = []
            all_data = loadData(categoria = st_categoria, ordem=ordem)
            
    else:
         flash(slc_category.errors)




    
    if slc_options.validate_on_submit():
        st_opcoes = slc_options.data['opcoes']
        if st_opcoes == 'Mais Recentes':
            ordem = Post.data_hora.desc()
        elif st_opcoes == 'Mais Antigos':
            ordem = Post.data_hora.asc()
        elif st_opcoes == 'A-z':
            ordem = Post.titulo.asc()
        elif st_opcoes == 'Z-a':
            ordem = Post.titulo.desc()

        if st_opcoes != "Todos":
            all_data = []
            all_data = loadData(categoria=st_categoria,estado=st_estado,ordem=ordem)
        
        else:
            all_data = []
            all_data = loadData(categoria = st_categoria, estado=st_estado)
    else:
         flash(slc_category.errors)


    if form.busca.data and form.validate():
        search = db.session.query(Post).join(User).join(Category).filter(Post.titulo.like(f"%{form.busca.data}%")).all()
        if search != '':
            print(search)
            modified_data = []
            all_data = []
            for item in search:
                modified_data = []
                modified_data.append(item.titulo)
                modified_data.append(item.descricao)
                modified_data.append(base64.b64encode(item.img_1).decode('ascii'))
                modified_data.append(item.data_hora)
                modified_data.append(item.user.estado)
                modified_data.append(item.user.cidade)
                modified_data.append(item.categoria.nome_categoria)
                modified_data.append(item.get_id())

                all_data.append(modified_data)
        else:
            pass
    else:
        print(form.errors)


    num_posts = len(all_data)
    print(f"Total de anuncios:{num_posts}")

    return render_template("busca.html", form=form, slc_category=slc_category,estado = slc_state,slc_options=slc_options, data=all_data, st_categoria=st_categoria,st_estado=st_estado, num_posts = num_posts)



'''
Carrega função para encerrar sessão de usuário
'''
@app.route("/logout")
def logout():
    logout_user()
    flash("Usuario deslogado")
    return redirect(url_for("index"))



'''
Página de confirmação de cadastro
'''
@app.route("/register")
def register():
    return render_template("cadastro.html")



'''
Página dinâmica para os produtos cadastrados
'''
@app.route("/product/<info>")
def product(info):
    post= db.session.query(Post).join(User).join(Category).filter(Post.id_post==int(info)).first()
    imagem = base64.b64encode(post.img_1).decode('ascii')
    
    return render_template("product.html",data=post, imagem=imagem)

'''
Página dinâmica para editar os produtos cadastrados
'''
@app.route("/edit_product/<info>", methods=["GET","POST"])
def edit_product(info):
    
    post= db.session.query(Post).join(User).join(Category).filter(Post.id_post==int(info)).first()

    form = PostForm(titulo=post.titulo,descricao=post.descricao,img_1=post.img_1,categorias=post.id_categoria)

    imagem = base64.b64encode(post.img_1).decode('ascii')

    if form.validate_on_submit():
        if request.method == 'POST' and form.img_1.data != '':
            image_data = request.files[form.img_1.name].read()
            post.img_1 = image_data
        post.titulo = form.titulo.data
        post.descricao = form.descricao.data
        post.id_categoria = form.categorias.data
        db.session.add(post)
        db.session.commit()
        flash("Item atualizado com sucesso","alert alert-success")
        return redirect(url_for("user_post"))

    else:
        if form.errors:
            flash(str(form.errors),"alert alert-danger")
    
    
    return render_template("edit-product.html",form=form,data=post,imagem=imagem)

@app.route("/delete_product/<info>", methods=["GET","POST"])
def delete_product(info):
    
    query= db.session.query(Post).filter(Post.id_post==int(info)).delete()
    db.session.commit()
    flash(f"Item deletado","alert alert-warning")
    return redirect(url_for("user_post"))
    



@app.route("/popup/<info>", methods=["GET","POST"])
def popup(info):

    return render_template('popup.html',id=info)



'''
Página para o usuário logado inserir um novo anuncio de um item que deseja doar
'''
@app.route("/user-new-post", methods=["GET","POST"])
def user_new_post():
    form = PostForm()
    
    if form.validate_on_submit():
        
        if request.method == 'POST':
            image_data = request.files[form.img_1.name].read()
        
        p = Post(form.titulo.data, form.descricao.data, image_data, id_usuario=int(current_user.get_id()),id_categoria=int(form.categorias.data) )
        db.session.add(p)
        db.session.commit()
        flash("Anúncio cadastrado com sucesso!")
        return redirect(url_for('user_post'))
    else:
        flash(form.errors)

    return render_template("user-new-post.html",form=form)



'''
Página para o usuário logado verificar os seus anuncios ativos, editar ou excluir, caso desejar
'''
@app.route("/user-post", methods=["GET","POST"])
def user_post():
    user = current_user.email
    
    data = db.session.query(Post).join(User).join(Category).filter(
        User.email == user).order_by(Post.data_hora.desc()).all()
    modified_data = []
    all_data = []
    for item in data:
        modified_data = []
        modified_data.append(item.titulo)
        modified_data.append(item.descricao)
        modified_data.append(base64.b64encode(item.img_1).decode('ascii'))
        modified_data.append(item.data_hora)
        modified_data.append(item.user.estado)
        modified_data.append(item.user.cidade)
        modified_data.append(item.categoria.nome_categoria)
        modified_data.append(item.get_id())

        all_data.append(modified_data)
    
    return render_template("user-post.html", data=all_data)



'''
Página para o usuário logado editar suas informações de perfil
'''
@app.route("/user-profile", methods=["GET","POST"])
def user_profile():

    form = UserEditForm(name=current_user.nome.capitalize(),last_name=current_user.sobrenome.title(), email=current_user.email,
                        phone_number=current_user.telefone,cep=current_user.cep, estado=current_user.estado,
                        cidade=current_user.cidade,bairro=current_user.bairro)

    if form.validate_on_submit():
        form.validate_estado(form.estado)
        
        r= User.query.filter_by(id_usuario=int(current_user.get_id())).first()
        r.nome = form.name.data
        r.sobrenome = form.last_name.data
        r.email = form.email.data
        r.telefone = form.phone_number.data
        r.cep = form.cep.data
        r.estado = form.estado.data
        r.cidade = form.cidade.data
        r.bairro = form.bairro.data
        db.session.add(r)
        db.session.commit()
        flash("Cadastro atualizado com sucesso","alert alert-success")
    else:
        if form.errors:
            flash("Selecione uma opção válida","alert alert-danger")

    return render_template("user-profile.html",form=form)


'''
Função para obter dados sobre os itens cadastrados de acordo com os filtros selecionados
'''
def loadData(categoria="", estado="", ordem=Post.data_hora.desc()):
    if categoria == "Todas":
        categoria = ""

    if estado == "Todos":
        estado = ""


    data = db.session.query(Post).join(User).join(Category).filter(
        Category.nome_categoria.like(f'%{categoria}%'),
        User.estado.like(f'%{estado}%')).order_by(ordem).all()

    modified_data = []
    all_data = []
    for item in data:
        modified_data = []
        modified_data.append(item.titulo)
        modified_data.append(item.descricao)
        modified_data.append(base64.b64encode(item.img_1).decode('ascii'))
        modified_data.append(item.data_hora)
        modified_data.append(item.user.estado)
        modified_data.append(item.user.cidade)
        modified_data.append(item.categoria.nome_categoria)
        modified_data.append(item.get_id())

        all_data.append(modified_data)
    
    return all_data





