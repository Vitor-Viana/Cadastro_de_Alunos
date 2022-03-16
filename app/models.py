from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

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

users = {
            'vitor@gmail.com':{'senha':'vitor1998', 'nome':'Vítor Viana'}, 
            'hillary@gmail.com':{'senha':'hillary2002', 'nome':'Hillary Santos'}
        }
class User(UserMixin):
    pass
