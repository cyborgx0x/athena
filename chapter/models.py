from app.models import BaseModel
from sqlalchemy import String, Column, JSON, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


class Chapter(BaseModel):
    name: str = Column(String(255))
    short_desc = Column(String(160))
    content = Column(JSON)
    fiction_id = Column(UUID, ForeignKey('fiction.id'))

    @staticmethod
    def serializer(query):
        return [
            chapter.unpack() for chapter in query
        ]

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
            "short_desc",
        ]