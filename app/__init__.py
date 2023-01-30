from configuration import Config
from flask import Flask
from tools.text_processing import Process
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from dotenv import load_dotenv
from auth.auth import auth_bp


load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)
login.login_view = 'login'
Markdown(app)
Process(app)
app.register_blueprint(auth_bp)
from app import models, routes
