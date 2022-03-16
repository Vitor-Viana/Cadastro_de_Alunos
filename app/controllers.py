from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from os import remove
from app import app, login_manager
from app.models import db, users, Pessoa, User
from flask_login import login_user, current_user, logout_user

@login_manager.user_loader
def user_loader(email):
    user = User()
    user.id = email
    user.nome = users[email]['nome']
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['password']
        
        if email in users:
            if senha == users[email]['senha']:
                login_user(user_loader(email))
                return redirect(url_for('index'))    
        return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html")
    return redirect(url_for("login"))

@app.route("/cadastrar")
def  cadastrar():
    if current_user.is_authenticated:
        return render_template("cadastro.html")
    return redirect(url_for("login"))

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        file = request.files['identidade']

        if nome and telefone and cpf and email and file.filename != '':
            p = Pessoa(nome, telefone, cpf, email)
            db.session.add(p)
            db.session.commit()
            
            # Armazenando nome do arquivo identidade no banco de dados
            p.identidade = str(p._id) + '-' + file.filename
            db.session.commit()

            # Armazenando arquivo identidade no diretório
            file.save('./app/data/' + p.identidade)

    return redirect(url_for("index"))

@app.route("/lista")
def lista():
    if current_user.is_authenticated:
        pessoas = Pessoa.query.all()
        return render_template("lista.html", pessoas=pessoas)
    return redirect(url_for("login"))

@app.route("/excluir/<int:id>")
def excluir(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()
    remove('./app/data/' + pessoa.identidade)
    db.session.delete(pessoa)
    db.session.commit()

    return redirect(url_for("lista"))

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    if current_user.is_authenticated:
        pessoa = Pessoa.query.filter_by(_id=id).first()

        if request.method == "POST":
            nome = request.form.get("nome")
            telefone = request.form.get("telefone")
            cpf = request.form.get("cpf")
            email = request.form.get("email")
            file = request.files['identidade']
        
            if nome and telefone and cpf and email:
                pessoa.nome = nome
                pessoa.telefone = telefone
                pessoa.cpf = cpf
                pessoa.email = email
                db.session.commit()
            
                # Atualizando identidade no diretório e no banco de dados
                if file.filename != '':
                    remove('./app/data/' + pessoa.identidade)
                    pessoa.identidade = str(pessoa._id) + '-' + file.filename
                    db.session.commit()
                    file.save('./app/data/' + pessoa.identidade)

                return redirect(url_for("lista"))

        return render_template("atualizar.html", pessoa=pessoa)
    else:
        return redirect(url_for("login"))

@app.route('/exibirIdentidade/<name>')
def exibirIdentidade(name):
    if current_user.is_authenticated:
        return send_from_directory("./data", name)
    else:
        return redirect(url_for("login"))
        