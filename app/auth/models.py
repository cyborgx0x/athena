from sqlalchemy import (
    Column, Integer, String, Unicode, DateTime, JSON
)
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from sqlalchemy.dialects.postgresql import UUID
import requests
from app.models import BaseUser
from app.repo import UnPack


class CoreUser(BaseUser, UnPack):
    facebook = Column(String(50))
    name = Column(Unicode(256))
    username: str = Column(String(64))
    email = Column(String(120))
    avatar = Column(String(200))
    about_me = Column(JSON)
    last_seen = Column(DateTime, default=db.func.now())
    password_hash = db.Column(db.Text)
    type = Column(Integer, default=2)
    is_active = db.Column(db.Boolean, default=True, server_default="true")
    roles = db.Column(db.Text)

    @property
    def identity(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has an ``identity`` instance
        attribute or property that provides the unique id of the user instance
        """
        return str(self.id)

    @property
    def rolenames(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``rolenames`` instance
        attribute or property that provides a list of strings that describe the roles
        attached to the user instance
        """
        try:
            return self.roles.split(",")
        except Exception:
            return []
    
    @property
    def password(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``password`` instance
        attribute or property that provides the hashed password assigned to the user
        instance
        """
        return self.password_hash
    
    @classmethod
    def lookup(cls, username):
        """
        *Required Method*

        flask-praetorian requires that the user class implements a ``lookup()``
        class method that takes a single ``username`` argument and returns a user
        instance if there is one that matches or ``None`` if there is not.
        """
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        """
        *Required Method*

        flask-praetorian requires that the user class implements an ``identify()``
        class method that takes a single ``id`` argument and returns user instance if
        there is one that matches or ``None`` if there is not.
        """
        return cls.query.get(id)

    def is_valid(self):
        return self.is_active

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def load_avatar(self):
        if self.avatar:
            return self.avatar
        else:
            r = requests.get("https://api.thecatapi.com/v1/images/search")
            if r.status_code == 200:
                link = r.json()
                link = link[0]
                link = dict(link)["url"]
                return link

    class Meta:
        fields = [
            "id",
            "name",
            "username",
            "email",
            "avatar",
            "created_at",
        ]
