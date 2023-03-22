
from flask import Blueprint
from fiction.views import FictionItemView, FictionListAPIView
from fiction.models import Fiction
fiction = Blueprint("fiction", __name__, template_folder="templates", static_folder='static')


fiction.add_url_rule("/fictions/<int:id>", view_func=FictionItemView.as_view("fiction_item", Fiction))
fiction.add_url_rule("/fictions/", view_func=FictionListAPIView.as_view("fiction_list", Fiction))
