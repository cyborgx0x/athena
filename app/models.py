from sqlalchemy import Column, Integer, String, Unicode, JSON, DateTime
import requests
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime
from tools import *
from dataclasses import dataclass
from markupsafe import Markup
from sqlalchemy import (MetaData, Text, Unicode, UnicodeText,
                        JSON, Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.dialects.postgresql import UUID
from app import db, login
import uuid
import json
meta = MetaData()
from sqlalchemy.ext.declarative import declared_attr


class BaseModel(db.Model):
    '''
    provide basic attribute for model
    '''
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=db.func.now())
    modified_at = Column(DateTime, default=db.func.now(), onupdate=db.func.now())
    @declared_attr
    def created_by(cls):
        return Column(Integer, ForeignKey('user.id'))

    def update_from_json(self, data:dict):
        for key, value in data.items():
            self.__setattr__(key,value)

    @staticmethod
    def from_json(json_data):
        return __class__(**json_data)
@dataclass
class Collection(db.Model):

    '''
    Collection has all document metadata

    It can apply to many type of document: book, project, fiction, screenplay
    It provide basic functionality as:

    method: from_json 
    - param: json_data: A Json Data from client to create new collection
    

    '''
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(Unicode(300))
    tag: str = Column(Unicode(300))
    status: str = Column(Unicode(300), default="draft")
    short_desc: str = Column(String(160))
    desc: dict = Column(JSON)
    cover_data: dict = Column(JSON)
    cover: str = Column(Text)
    download: str = Column(Unicode(500))
    time = Column(DateTime, default=datetime.now())
    view: int = Column(Integer)
    creator_id = Column(Integer, ForeignKey('user.id'))
    type_id = Column(Integer, ForeignKey('type.id'))
    media = db.relationship('Media', backref='collection')

    @staticmethod
    def from_json(json_data):
        return __class__(**json_data)

    def to_json(self):
        return self

    def tag_render(self):
        try:
            passing_array = self.tag.split(", ")
            return passing_array
        except:
            return "No tag"

@dataclass
class User(UserMixin, db.Model):

    '''
    the owner of asset, this table contain the basic information of user, and connect user with the action he can do in the application
    such as: like, follow, create, update, delete. 
    '''

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    facebook = Column(String(50))
    name = Column(Unicode(256))
    user_name: str = Column(String(64))
    email = Column(String(120))
    avatar = Column(String(200))
    about_me = Column(JSON)
    last_seen = Column(DateTime, default=datetime.utcnow)
    password_hash = Column(String(128))
    type = Column(Integer, default=2)
    '''
    user action
    '''
    media = relationship('Media', backref='owner')
    collection = relationship('Collection', backref='owner')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def load_avatar(self):
        if self.avatar == None:
            r = requests.get("https://api.thecatapi.com/v1/images/search")
            if r.status_code == 200:
                link = r.json()
                link = link[0]
                link = dict(link)["url"]
                return link
        else:
            return self.avatar


@dataclass
class Media(db.Model):
    '''
    media is core table of the application, it contain the element that construct the collection, and can be reuse anywhere by the creator
    media can be: link, audio, text content, image, array of images
    media can contain media???
    this table connect with collection thought collection_id, the basic meta is: name, content, type.
    content column is json format.
    '''

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(160))
    short_desc = Column(String(160))
    content = Column(JSON)
    type = Column(String(50))
    time = Column(DateTime, default=datetime.now())
    '''
    statistic column
    '''
    view = Column(Integer)
    '''
    one to many relationship
    '''
    collection_id = Column(Integer, ForeignKey('collection.id'))
    user_id = Column(Integer, ForeignKey('user.id'))


@dataclass
class Type(db.Model):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(160))
    short_desc = Column(String(160))
    slug = Column(String(160))
    collection = db.relationship('Collection', backref='type')
