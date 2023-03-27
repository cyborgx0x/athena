import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:////tmp/test.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ACCESS_LIFESPAN =  {"hours": 24}
    JWT_REFRESH_LIFESPAN = {"days": 30}
    class ArticleConstant:
        DRAFT = "draft"
        PUBLIC = "public"
        