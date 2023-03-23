from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, DateTime
from sqlalchemy import (MetaData, 
                        Column, DateTime, ForeignKey)
from sqlalchemy.dialects.postgresql import UUID
from app import db
import uuid

meta = MetaData()

class BaseUser(db.Model):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    created_at = Column(DateTime, default=db.func.now())
    modified_at = Column(DateTime, default=db.func.now(),
                         onupdate=db.func.now())

class BaseModel(db.Model):
    '''
    provide basic attribute for model
    '''
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    created_at = Column(DateTime, default=db.func.now())
    modified_at = Column(DateTime, default=db.func.now(),
                         onupdate=db.func.now())

    @declared_attr
    def created_by(cls):
        return Column(UUID, ForeignKey("core_user.id"))
