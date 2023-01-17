from flask_sqlalchemy import SQLAlchemy
from typing import Any
from .request import Request

class Repo():
    def __init__(self, db:SQLAlchemy, model: Any ) -> None:
        self.db = db
        self.model = model
    
    def save(self, request: Request):
        hm = request.to_dict()
        status  = []
        for i,j in hm.items():
            self.model.__setattr__(i,j)
            status.append(f"{i} has been saved")
        self.db.session.commit()
        return status