from flask import Blueprint, request, jsonify
from app import db
from chapter.models import Chapter
from flask_login import login_required

chapter = Blueprint("chapter", __name__, template_folder="templates", static_folder='static')

@chapter.route("/chapters/", methods=['GET', 'POST'])
# @login_required
def list_and_create_chapter():
    if request.method == "POST":
        new_chapter = Chapter.from_json(request.json)
        db.session.add(new_chapter)
        db.session.commit()
        return jsonify(new_chapter.unpack())
    else:
        page  = request.args.get("page", 1, type=int)
        query = Chapter.query.paginate(page=page,per_page=4, error_out = False)
        return Chapter.serializer(query.items)
