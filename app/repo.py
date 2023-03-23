'''
Tool to serialize model and return to API VIEW
'''

from flask_sqlalchemy import SQLAlchemy
from typing import Any
from .request import Request


class Repo():
    def __init__(self, db: SQLAlchemy, model: Any) -> None:
        self.db = db
        self.model = model

    def save(self, request: Request):
        hm = request.to_dict()
        for i, j in hm.items():
            self.model.__setattr__(i, j)
        self.db.session.commit()



class UnPack():
    '''
    This module provide handy method for model to load from validated data
    It also return the instance in JSON with the fields declared in Meta
    '''
    class Meta:
        pass

    @staticmethod
    def serializer(query):
        return [
            item.to_json() for item in query
        ]

    def update_from_json(self, data: dict):
        for key, value in data.items():
            self.__setattr__(key, value)

    def to_json(self):
        return {
            field: self.__getattribute__(field) for field in self.Meta.fields
        }
