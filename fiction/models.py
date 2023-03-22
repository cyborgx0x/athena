from app.models import Collection
from app import db
from sqlalchemy import (Text, Column, Integer)
                        
class Fiction(Collection):
    def update_from_json(self, data:dict):
        for key, value in data.items():
            self.__setattr__(key,value)


class Test (db.Model):
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)