'''
take the request from client, validate and return in Data Model

'''

from werkzeug.datastructures import ImmutableMultiDict
import json
from flask_sqlalchemy import SQLAlchemy

class Request(object):
    fields:dict = {}
    def __init__(self, db: SQLAlchemy, model) -> None:
        self.db = db
        self.model = model
        print()
    def populate(self, request: ImmutableMultiDict) -> bool:
        pass
    def validate(self):
        '''
        validate the field include in the fields
        '''
        pass
    def sanitize(self):
        pass
    def to_dict(self):
        pass
    def save(self):
        hm = self.to_dict()
        for i,j in hm.items():
            self.model.__setattr__(i,j)
        self.db.session.commit()
        print(f"Update {self.model} completed")

class Collection_Request(Request):
    fields = {
        "collection_name": "name",
        "tag-manage": "tag",
        "book-cover":"cover",
        "short-desc": "short_desc",
        "download": "download",
        "collection-theme": "",
    }
    def populate(self, request: ImmutableMultiDict) -> bool:
        super().populate(request)
        for i in self.fields.keys():
            value = request.get(key=i)
            field = self.fields.get(i)
            self.__setattr__(field, value)
        return True
    def sanitize(self) -> bool:
        super().sanitize()
        pass
    def to_dict(self) -> dict:
        hm = {}
        for i,v in self.fields.items():
            value = self.__getattribute__(v)
            if value != "None" and value != None:
                hm[v] = value
        return hm
