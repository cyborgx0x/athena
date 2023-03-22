from app.models import BaseModel
from sqlalchemy import String, Column, JSON, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

class Chapter(BaseModel):
    name: str = Column(String(255))
    short_desc = Column(String(160))
    content = Column(JSON)
    fiction_id = Column(UUID, ForeignKey('fiction.id'))
    