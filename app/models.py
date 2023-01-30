from dataclasses import dataclass
from markupsafe import Markup
from sqlalchemy import MetaData, Text, Unicode, UnicodeText, JSON, Column, Integer, String, DateTime, ForeignKey
from flask_sqlalchemy import Model
from app import db, login
import json
meta = MetaData()
from tools import *
from datetime import datetime
@dataclass
class Collection(db.Model):
    
    '''
    This table contain many element, and bundle it into a collection, which can be show as a book, project, fiction, screenplay
    Data of this table can be access directly throught search filter, have it own style that affect the whole. 
    '''
    id:int = Column(Integer, primary_key=True, autoincrement=True)
    name:str = Column(Unicode(300))
    tag:str = Column(Unicode(300))
    status = Column(Unicode(300), default ="draft")
    short_desc:str = Column(String(160))
    desc = Column(JSON)
    cover_data = Column(JSON)
    cover:str = Column(Text)
    download = Column(Unicode(500))
    time = Column(DateTime, default=datetime.now())
    view = Column(Integer)
    creator_id = Column(Integer, ForeignKey('user.id'))
    type_id = Column(Integer, ForeignKey('type.id'))
    media = db.relationship('Media', backref ='collection')
    def create(self, *args, **kwargs):
        pass
    def tag_render(self):
        try: 
            passing_array = self.tag.split(", ")
            return passing_array
        except:
            return "No tag"
    def save(self, passing):
        '''
        take an passing data and set the instance data to the passing data, return message to the user
        '''
        incoming_data= json.loads(passing.decode('UTF-8'))
        name = incoming_data["type"]
        print(self.desc['blocks'])
        return "success"
    def render_text(self):
        render = []
        for item in self.desc["blocks"]:
            if item["type"] == "paragraph":
                render.append("<p>" + item["data"]["text"] + "</p>")
            elif item["type"] == "header":
                render.append("<h2>" + item["data"]["text"] + "</h2>")
            elif item["type"] == "list":
                render.append(str(item["data"]))
            elif item["type"] == "image":
                render.append("<img class='render-image' src='{0}'>".format(item["data"]["file"]["url"]))
        output = "\n".join(render)
        return Markup(output)




from flask_login import UserMixin
from sqlalchemy.orm import DeclarativeBase, relationship
from dataclasses import dataclass
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import requests

from sqlalchemy import Column, Integer, String, Unicode, JSON, DateTime
# from app import login

class Base(DeclarativeBase):
    pass

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
    last_seen = Column(DateTime, default = datetime.utcnow)
    password_hash = Column(String(128))
    type = Column(Integer, default = 2)
    '''
    user action
    '''
    media = relationship('Media', backref ='owner')
    collection = relationship('Collection', backref ='owner')
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
class Type(db.Model):
    id:int = Column(Integer, primary_key=True, autoincrement=True)
    name:str = Column(String(160))
    short_desc = Column(String(160))
    slug = Column(String(160))
    collection = db.relationship('Collection', backref ='type')
