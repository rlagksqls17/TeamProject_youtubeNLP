from evereview.db_connect import db


class Channel(db.Model):

    __tablename__ = "channel"

    id = db.Column(db.String(128), primary_key=True, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    title = db.Column(db.String(128), nullable=False)
    channel_url = db.Column(db.String(1024), nullable=False)
    img_url = db.Column(db.String(1024), nullable=False)
    comment_count = db.Column(db.Integer, nullable=False)
    video_count = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        result = {
            "id": self.id,
            "title": self.title,
            "channel_url": self.channel_url,
            "img_url": self.img_url,
            "comment_count": self.comment_count,
            "video_count": self.video_count,
        }

        return result
