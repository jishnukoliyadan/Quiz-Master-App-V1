
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

DB_NAME = 'quizapp.db'
app = Flask(__name__, template_folder = 'templates')

app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

db = SQLAlchemy()
bcrypt = Bcrypt(app)

db.init_app(app)
app.app_context().push()