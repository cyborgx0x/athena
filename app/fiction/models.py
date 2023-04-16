from app.models import BaseModel
from app import db
from configuration import Config
from sqlalchemy import (Text, Column, Integer, Unicode,
                        JSON, String
                        )
from sqlalchemy.orm import relationship
from app.chapter.models import Chapter
from app.repo import UnPack
class Fiction(BaseModel, UnPack):
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
    def from_json(json_data: dict):
        return __class__(**json_data)
    class Meta:
        fields = [
            "id",
            "name",
            "tag",
            "status",
            "short_desc",
            "desc",
        ]