from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from os import remove

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class Pessoa(db.Model):
    __tablename__ = 'cliente'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    telefone = db.Column(db.String)
    cpf = db.Column(db.String)
    email = db.Column(db.String)
    identidade = db.Column(db.String)

    def __init__(self, nome, telefone, cpf, email):
        self.nome = nome
        self.telefone = telefone
        self.cpf = cpf
        self.email = email

db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastrar")
def  cadastrar():
    return render_template("cadastro.html")

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
            file.save('./data/' + p.identidade)

    return redirect(url_for("index"))

@app.route("/lista")
def lista():
    pessoas = Pessoa.query.all()
    return render_template("lista.html", pessoas=pessoas)

@app.route("/excluir/<int:id>")
def excluir(id):
    pessoa = Pessoa.query.filter_by(_id=id).first()
    remove('./data/' + pessoa.identidade)
    db.session.delete(pessoa)
    db.session.commit()

    return redirect(url_for("lista"))
 
@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
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
                remove('./data/' + pessoa.identidade)
                pessoa.identidade = str(pessoa._id) + '-' + file.filename
                db.session.commit()
                file.save('./data/' + pessoa.identidade)

            return redirect(url_for("lista"))

    return render_template("atualizar.html", pessoa=pessoa)

@app.route('/exibirIdentidade/<name>')
def exibirIdentidade(name):
    return send_from_directory("./data", name)

if __name__ == '__main__':
    app.run(debug=True)
