'''
Collection of tool to work with request HTTP
'''

from werkzeug.datastructures import ImmutableMultiDict
import json
from flask_sqlalchemy import SQLAlchemy

class Request():
    '''
    Turn the request to one unified data type
    '''
    fields:dict = {}
    
    def populate(self, request: ImmutableMultiDict) -> dict:
        for i in self.fields.keys():
            value = request.get(key=i)
            field = self.fields.get(i)
            self.__setattr__(field, value)
        return self
    
    @staticmethod
    def byte_handle(self, request: bytes) -> bool:
        st = request.decode("UTF-8")
        data:dict = json.loads(st)
        for i in self.fields.keys():
            value = data.get(i)
            field = self.fields.get(i)
            self.__setattr__(field, value)
        return True
        
    def to_dict(self) -> dict:
        hm = {}
        for i,v in self.fields.items():
            value = self.__getattribute__(v)
            if value != "None" and value != None:
                hm[v] = value
        return hm
    class Meta:
        fields = list

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
