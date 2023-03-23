from sqlalchemy import (
    Column, Integer, String, Unicode, DateTime, JSON
)
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from sqlalchemy.dialects.postgresql import UUID
import requests
from app.models import BaseUser
from app.repo import UnPack
from app import login

class CoreUser(UserMixin, BaseUser, UnPack):
    facebook = Column(String(50))
    name = Column(Unicode(256))
    user_name: str = Column(String(64))
    email = Column(String(120))
    avatar = Column(String(200))
    about_me = Column(JSON)
    last_seen = Column(DateTime, default=db.func.now())
    password_hash = Column(String(128))
    type = Column(Integer, default=2)

    @login.user_loader
    def load_user(id):
        return CoreUser.query.get(id)

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
            "user_name",
            "email",
            "avatar",
            "created_at",
        ]
