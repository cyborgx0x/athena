from app.models import BaseModel
from app import db
from configuration import Config
from sqlalchemy import (Text, Column, Integer, Unicode,
                        JSON, String
                        )
from sqlalchemy.orm import relationship
from chapter.models import Chapter

class Fiction(BaseModel):
    name: str = Column(Unicode(300))
    tag = Column(JSON)
    status: str = Column(Unicode(125), default=Config.ArticleConstant.DRAFT)
    short_desc: str = Column(String(160))
    desc = Column(JSON)
    cover_data: str = Column(Unicode(300))
    cover: str = Column(Text)
    download: str = Column(Unicode(500))
    view: int = Column(Integer)
    chapter = relationship(Chapter, backref='fiction')
    
    @staticmethod
    def from_json(json_data):
        return __class__(**json_data)
    
    def unpack(self):
        return {
            field:self.__getattribute__(field) for field in self.Meta.fields
        }
    class Meta:
        fields = [
            "id",
            "name",
            "tag",
            "status",
            "short_desc",
            "desc",
        ]