from flask import Blueprint, request, jsonify
from app import db
from chapter.models import Chapter
from flask_login import login_required
from app.views import register_api


chapter = Blueprint("chapter", __name__, template_folder="templates", static_folder='static')

register_api(app=chapter, model=Chapter, name="chapters")
