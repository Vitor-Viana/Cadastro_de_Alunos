from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class Pessoa(db.Model):
    __tablename__ = 'aluno'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    idade = db.Column(db.String)
    peso = db.Column(db.String)
    altura = db.Column(db.String)
    faixa = db.Column(db.String)
    grau = db.Column(db.String)
    telefone = db.Column(db.String)
    cpf = db.Column(db.String)
    email = db.Column(db.String)
    identidade = db.Column(db.String)
    presenca = db.Column(db.String)
    falta = db.Column(db.String)
    tot_presenca = db.Column(db.String)
    tot_falta = db.Column(db.String)

    def __init__(self, nome, idade, peso, altura, faixa, grau, telefone, cpf, email):
        self.nome = nome
        self.idade = idade
        self.peso = peso
        self.altura = altura
        self.faixa = faixa
        self.grau = grau
        self.telefone = telefone
        self.cpf = cpf
        self.email = email
        self.presenca = "0@0@0@0@0@0@0@0@0@0@0@0"
        self.falta = "0@0@0@0@0@0@0@0@0@0@0@0"
        self.tot_presenca = "0"
        self.tot_falta = "0"

db.create_all()

users = {
            'admin':{'senha':'244872vitor', 'nome':'Vítor Viana'}, 
            'projetocjj':{'senha':'cjj2022', 'nome':'Projeto CJJ'}
        }
class User(UserMixin):
    pass
