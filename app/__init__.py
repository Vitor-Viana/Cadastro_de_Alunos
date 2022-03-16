from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'secret'
login_manager = LoginManager(app)

from app import controllers
