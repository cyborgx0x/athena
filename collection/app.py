
from flask import Blueprint
from collection.views import CollectionAPIView, CollectionListAPIView
from app.models import Collection

collection = Blueprint("collection", __name__, template_folder="templates", static_folder='static')


# collection.add_url_rule("/collections/", view_func=CollectionAPIView.as_view("collection_list", Collection))
collection.add_url_rule("/collections/", view_func=CollectionListAPIView.as_view("collection_list", Collection))
