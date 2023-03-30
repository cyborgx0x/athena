
from configuration import Config
from flask import Flask
from app.tools.text_processing import Process
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from dotenv import load_dotenv
from flask_cors import CORS
from flask_login import LoginManager

load_dotenv()
app = Flask(__name__)

CORS(app)
app.config.from_object(Config)
from flask_praetorian import Praetorian



db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth_bp.login'


Markdown(app)
Process(app)
# from app import models, routes