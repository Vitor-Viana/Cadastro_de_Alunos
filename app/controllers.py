from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from os import remove
from app import app, login_manager
from app.models import db, users, Pessoa, User
from flask_login import login_user, current_user, logout_user
from app.contador import totPresenca, totFalta, dataAtual

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

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        if request.method == "POST":
            nome = request.form.get("nome")
            idade = request.form.get("idade")
            peso = request.form.get("peso")
            altura = request.form.get("altura")
            faixa = request.form.get("faixa")
            grau = request.form.get("grau")
            telefone = request.form.get("telefone")
            cpf = request.form.get("cpf")
            email = request.form.get("email")
            file = request.files['identidade']

            if nome and telefone and cpf and email and idade and peso and altura and faixa and grau and file.filename != '':
                p = Pessoa(nome, idade, peso, altura, faixa, grau, telefone, cpf, email)
                db.session.add(p)
                db.session.commit()
                
                # Armazenando nome do arquivo identidade no banco de dados
                p.identidade = str(p._id) + '-' + file.filename
                db.session.commit()

                # Armazenando arquivo identidade no diretório
                file.save('./app/data/' + p.identidade)
                return redirect(url_for("index"))
        return render_template("cadastro.html")
    return redirect(url_for("login"))

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
            idade = request.form.get("idade")
            peso = request.form.get("peso")
            altura = request.form.get("altura")
            faixa = request.form.get("faixa")
            grau = request.form.get("grau")
            telefone = request.form.get("telefone")
            cpf = request.form.get("cpf")
            email = request.form.get("email")
            file = request.files['identidade']
        
            if nome and telefone and cpf and email and idade and peso and altura and faixa and grau:
                pessoa.nome = nome
                pessoa.idade = idade
                pessoa.peso = peso
                pessoa.altura = altura
                pessoa.faixa = faixa
                pessoa.grau = grau
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

        return redirect(f"/aluno/{id}")
    return redirect(url_for("login"))

@app.route("/aluno/<int:id>")
def aluno(id):
    if current_user.is_authenticated:
        pessoa = Pessoa.query.filter_by(_id=id).first()
        return render_template("aluno.html", pessoa=pessoa)
    return redirect(url_for("login"))

@app.route('/exibirIdentidade/<name>')
def exibirIdentidade(name):
    if current_user.is_authenticated:
        return send_from_directory("./data", name)
    return redirect(url_for("login"))

@app.route("/diario/<int:id>", methods=['GET', 'POST'])
def diario(id):
    mesAtual = int(dataAtual().split('/')[1]) - 1
    meses = ('Janeiro', 'Fevereiro', 'Março', 'Abril',
             'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro',
             'Outubro', 'Novembro', 'Dezembro')
    aluno = Pessoa.query.filter_by(_id=id).first()
    vet_presenca = list()
    vet_falta = list()

    if request.method == "POST":
        presente = request.form.get("presente")
        falta = request.form.get("falta")
        if presente:
            presenca = aluno.presenca.split('@')
            presenca[mesAtual] = str(int(presenca[mesAtual])+1)
            # Calculando o total de presença
            aluno.tot_presenca = totPresenca(presenca)

            presenca = '@'.join(presenca)
            aluno.presenca = presenca
           
            db.session.commit()
            return redirect(url_for("lista"))
        
        if falta:
            falta = aluno.falta.split('@')
            falta[mesAtual] = str(int(falta[mesAtual])+1)
            # Calculando o total da falta
            aluno.tot_falta = totFalta(falta)
            
            falta = '@'.join(falta)
            aluno.falta = falta
            
            db.session.commit()
            return redirect(url_for("lista"))
           
        for i in range(1, 13):
            num_presenca = request.form.get("pMes"+str(i))
            num_falta = request.form.get("fMes"+str(i))
            if num_presenca:
                vet_presenca.append(num_presenca)
            else:
                vet_presenca.append('0')
            if num_falta:
                vet_falta.append(num_falta)
            else:
                vet_falta.append('0')
        aluno.presenca = '@'.join(vet_presenca)
        aluno.falta = '@'.join(vet_falta)
        # Calculando o total de presença e falta
        aluno.tot_presenca = totPresenca(vet_presenca)
        aluno.tot_falta = totFalta(vet_falta)
       
        db.session.commit()

    return render_template(
                            "diario.html", 
                            aluno=aluno, 
                            meses=meses,
                            presenca=aluno.presenca.split('@'),
                            falta=aluno.falta.split('@'),
                            dataAtual=dataAtual())
