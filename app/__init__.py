from configuration import Config
from flask import Flask
from tools.text_processing import Process
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)

CORS(app)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'
Markdown(app)
Process(app)

from app import models, routes
