'''
Collection of tool to work with request HTTP
'''

from werkzeug.datastructures import ImmutableMultiDict
import json


class Request():
    '''
    Turn the request to one unified data type
    '''
    def populate(self):
        '''
        This will populate field in register_fields to the objects
        For now I dont have any idea to working with it, even it can provide type check for each field
        '''
        pass

    def to_json(self, load_of_data: ImmutableMultiDict) -> dict:
        return {
            counter_field: load_of_data.get(field) for (field, counter_field) in self.Meta.register_fields.items()
        }
    
    def byte_handle(self, request: bytes) -> dict:
        st = request.decode("UTF-8") 
        return self.to_json(load_of_data=json.loads(st))

    class Meta:
        fields = list
        register_fields = dict


class Collection_Request(Request):
    class Meta:
        register_fields = {
            "collection_name": "name",
            "tag-manage": "tag",
            "book-cover": "cover",
            "short-desc": "short_desc",
            "download": "download",
            "collection-theme": "",
            "status": "status",
            "content": "desc",
        }


class Media_Request(Request):
    class Meta:
        register_fields = {
            "chapter_name": "name",
            "chapter_order": "chapter_order",
            "upload": "content",
        }

