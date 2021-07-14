from dataclasses import dataclass
from datetime import datetime
from re import T
from flask_login import UserMixin
from sqlalchemy import MetaData, Text, Unicode, UnicodeText, JSON, Column, Integer, String, DateTime, ForeignKey
from flask_sqlalchemy import Model
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login
import json
import requests
meta = MetaData()
from tools import *
import base64

@dataclass
class Collection(db.Model):
    
    '''
    This table contain many element, and bundle it into a collection, which can be show as a book, project, fiction, screenplay
    Data of this table can be access directly throught search filter, have it own style that affect the whole. 
    '''
    '''
    basic meta
    '''
    id:int = Column(Integer, primary_key=True, autoincrement=True)
    name:str = Column(Unicode(300))
    author:str = Column(Unicode(300))
    tag:str = Column(Unicode(300))
    status = Column(Unicode(300), default ="draft")
    short_desc:str = Column(String(160))
    desc = Column(JSON)
    cover_data = Column(JSON)
    cover:str = Column(Text)
    publish_year = Column(Integer)
    type = Column(String(50))
    download = Column(Unicode(500))
    '''
    statistic zone
    '''
    view = Column(Integer)
    creator_id = Column(Integer, ForeignKey('user.id'))
    media = db.relationship('Media', backref ='collection')
    def create(self, *args, **kwargs):
        pass
    def tag_render(self):
        passing_array = self.tag.split(", ")
        return passing_array
    def save(self, passing):
        '''
        take an passing data and set the instance data to the passing data, return message to the user
        '''
        incoming_data= json.loads(passing.decode('UTF-8'))
        name = incoming_data["type"]
        print(self.desc['blocks'])
        return "success"
    def render_cover(self):
        img = self.cover
        crop_image = return_img(img)
        file_data = base64.b64encode(crop_image.getvalue()).decode()
        data = {
            "image":file_data
        }
        api = "b4efdd223b0240f2b1212a0cef3bda37"
        link = "https://api.imgbb.com/1/upload?key="
        response = requests.post(link+api, data=data)
        self.cover_data = response.json()    





@dataclass
class Media(db.Model):
    '''
    media is core table of the application, it contain the element that construct the collection, and can be reuse anywhere by the creator
    media can be: link, audio, text content, image, array of images
    media can contain media???
    this table connect with collection thought collection_id, the basic meta is: name, content, type.
    content column is json format.
    '''
    
    id:int = Column(Integer, primary_key=True, autoincrement=True)
    name:str = Column(String(160))
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
class User(UserMixin, db.Model):
    '''
    the owner of asset, this table contain the basic information of user, and connect user with the action he can do in the application
    such as: like, follow, create, update, delete. 
    '''
    id:int = Column(Integer, primary_key=True, autoincrement=True)
    facebook = Column(String(50))
    name = Column(Unicode(256))
    user_name:str = Column(String(64))
    email = Column(String(120))
    avatar = Column(String(200))
    about_me = Column(JSON)
    last_seen = db.Column (DateTime, default = datetime.utcnow)
    password_hash = Column(String(128))
    type = Column(Integer, default = 2)
    '''
    user action
    '''
    media = db.relationship('Media', backref ='owner')
    collection = db.relationship('Collection', backref ='owner')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

