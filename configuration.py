import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = "postgres://fonnogzqihxzxw:834cd8df7070dc45cc7260cafa748f9e2ab6332e43ffd78bbeb70a52bc29adac@ec2-54-224-194-214.compute-1.amazonaws.com:5432/ddlhcbi93t3il7"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'