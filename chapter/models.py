from app.models import BaseModel
from sqlalchemy import String, Column, JSON, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.repo import UnPack

class Chapter(BaseModel, UnPack):
    name: str = Column(String(255))
    short_desc = Column(String(160))
    content = Column(JSON)
    fiction_id = Column(UUID, ForeignKey('fiction.id'))
    
    @staticmethod
    def from_json(json_data: dict):
        return __class__(**json_data)
    class Meta:
        fields = [
            "id",
            "name",
            "short_desc",
        ]