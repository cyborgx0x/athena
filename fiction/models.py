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
    tag: dict = Column(JSON)
    status: str = Column(Unicode(125), default=Config.ArticleConstant.DRAFT)
    short_desc: str = Column(String(160))
    desc: dict = Column(JSON)
    cover_data: str = Column(Unicode(300))
    cover: str = Column(Text)
    download: str = Column(Unicode(500))
    view: int = Column(Integer)
    chapter = relationship(Chapter, backref='fiction')
    view: int = Column(Integer)
