'''
take the request from client, validate and return in Data Model

'''

from werkzeug.datastructures import ImmutableMultiDict
import json
from flask_sqlalchemy import SQLAlchemy
from .process import ImageHandler

class Request(object):
    fields:dict = {}
    image: ImageHandler
    def populate(self, request: ImmutableMultiDict) -> bool:
        for i in self.fields.keys():
            value = request.get(key=i)
            field = self.fields.get(i)
            self.__setattr__(field, value)
        return True
    def byte_handle(self, request: bytes) -> None:
        st = request.decode("UTF-8")
        data:dict = json.loads(st)
        for i in self.fields.keys():
            value = data.get(i)
            field = self.fields.get(i)
            self.__setattr__(field, value)
        return True
    def image_upload(self):
        self.image.upload()
        if self.image.upload_status:
            self.__setattr__("cover", self.image.url)
        print(self.cover)
        
    def validate(self):
        '''
        validate the field include in the fields
        '''
        pass
    def sanitize(self):
        pass
    def to_dict(self) -> dict:
        hm = {}
        for i,v in self.fields.items():
            value = self.__getattribute__(v)
            if value != "None" and value != None:
                hm[v] = value
        return hm


class Collection_Request(Request):
    fields = {
        "collection_name": "name",
        "tag-manage": "tag",
        "book-cover":"cover",
        "short-desc": "short_desc",
        "download": "download",
        "collection-theme": "",
        "status": "status",
        "content": "desc",
    }


class Media_Request(Request):
    fields = {
        "chapter_name": "name",
        "chapter_order": "chapter_order",
        "upload": "content",
    }

