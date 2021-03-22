from flask import Flask, session, abort, g
from flask_sqlalchemy import SQLAlchemy
import os
#import psycopg2
# from flask_mail import Mail, Message
app = Flask(__name__)
secret_key = os.urandom(16)
app.secret_key = secret_key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ['DATABASE_URL'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database_two.db'
app.config['WTF_CSRF_ENABLED'] = False

app.config['SQLALCHEMY_BINDS'] = {
    'admin_db': 'sqlite:///database/database_two.db'
}

db = SQLAlchemy(app)
# mail = Mail(app)

from main import routes
