from evereview.db_connect import db


class Code(db.Model):

    __tablename__ = "code"

    id = db.Column(db.String(2), primary_key=True, nullable=False)
    description = db.Column(db.String(128), nullable=False)
