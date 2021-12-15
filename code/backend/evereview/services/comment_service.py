from evereview.models.comment import db, Comment


def get_comments(cluster_id):
    comments = Comment.query.filter_by(cluster_id=cluster_id).all()

    result = []
    for comment in comments:
        item = comment.to_dict()
        item["video"] = {
            "title": comment.video.title,
            "view_count": comment.video.view_count,
        }
        result.append(item)
    return result


def get_comment(cluster_id, comment_id):
    comment = Comment.query.filter_by(
        id=comment_id, cluster_id=cluster_id
    ).one_or_none()

    if comment is None:
        return comment

    result = comment.to_dict()
    result["video"] = {
        "title": comment.video.title,
        "view_count": comment.video.view_count,
    }
    return result


def insert_comment(**kwargs):
    try:
        new_comment = Comment(
            id=kwargs.get("comment_id"),
            cluster_id=kwargs.get("cluster_id"),
            video_id=kwargs.get("video_id"),
            author=kwargs.get("author"),
            author_img=kwargs.get("author_img"),
            text_display=kwargs.get("text_display"),
            text_original=kwargs.get("text_original"),
            like_count=kwargs.get("like_count"),
            published_at=kwargs.get("published_at"),
        )
        db.session.add(new_comment)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        raise error
