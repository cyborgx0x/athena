from configuration import Config
from flask import Flask
from app.tools.text_processing import Process
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

Markdown(app)
Process(app)
# from app import models, routes