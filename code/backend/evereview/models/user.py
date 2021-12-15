import json
from evereview.db_connect import db


class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    name = db.Column(db.String(32), nullable=False)
    img_url = db.Column(db.String(1024), nullable=False)
    nickname = db.Column(db.String(32), nullable=False)
    upload_term = db.Column(db.Integer, nullable=False)
    contents_category = db.Column(db.String(1024), nullable=False)
    oauth_token = db.Column(db.String(1024), nullable=True)
    access_token = db.Column(db.String(1024), nullable=True)
    refresh_token = db.Column(db.String(1024), nullable=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        result = {
            "email": self.email,
            "name": self.name,
            "img_url": self.img_url,
            "nickname": self.nickname,
            "upload_term": self.upload_term,
            "contents_category": json.loads(self.contents_category),
        }

        return result
