
from flask import Blueprint
from app.views import register_api
from fiction.models import Fiction
fiction = Blueprint("fiction", __name__, template_folder="templates", static_folder='static')

register_api(app=fiction, model=Fiction, name="fictions")