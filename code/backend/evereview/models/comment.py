from evereview.db_connect import db


class Comment(db.Model):

    __tablename__ = "comment"

    id = db.Column(db.String(128), primary_key=True, nullable=False)
    cluster_id = db.Column(
        db.String(128),
        db.ForeignKey("cluster.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    video_id = db.Column(
        db.String(128),
        db.ForeignKey("video.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    author = db.Column(db.String(128), nullable=False)
    author_img = db.Column(db.String(1024), nullable=False)
    text_display = db.Column(db.Text, nullable=False)
    text_original = db.Column(db.Text, nullable=False)
    like_count = db.Column(db.Integer, nullable=False)
    published_at = db.Column(db.DateTime(), nullable=False)

    video = db.relationship("Video", backref="video", lazy="joined")

    def to_dict(self):
        result = {
            "id": self.id,
            "cluster_id": self.cluster_id,
            "author": self.author,
            "author_img": self.author_img,
            "text_display": self.text_display,
            "text_original": self.text_original,
            "like_count": self.like_count,
            "published_at": self.published_at.isoformat(),
        }

        return result
