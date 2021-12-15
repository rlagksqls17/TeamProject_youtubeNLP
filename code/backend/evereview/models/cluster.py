from evereview.db_connect import db


class Cluster(db.Model):

    __tablename__ = "cluster"

    id = db.Column(db.String(128), primary_key=True, nullable=False)
    analysis_id = db.Column(
        db.String(128),
        db.ForeignKey("analysis.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    code = db.Column(
        db.String(2),
        db.ForeignKey("code.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    top_comment = db.Column(db.String(128), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    like_count = db.Column(db.Integer, nullable=False)
