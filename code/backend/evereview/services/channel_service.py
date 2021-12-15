from evereview.models.channel import db, Channel


def get_channel(channel_id):
    channel = Channel.query.filter_by(id=channel_id).one_or_none()

    return channel


def get_channels(user_id):
    result = []
    channels = Channel.query.filter_by(user_id=user_id).all()

    for channel in channels:
        result.append(channel.to_dict())

    return result


def insert_channel(**kwargs):
    try:
        new_channel = Channel(
            id=kwargs.get("channel_id"),
            user_id=kwargs.get("user_id"),
            title=kwargs.get("title"),
            comment_count=kwargs.get("comment_count")
            if kwargs.get("comment_count") is not None
            else 0,
            video_count=kwargs.get("video_count"),
            channel_url=kwargs.get("channel_url"),
            img_url=kwargs.get("img_url"),
        )
        db.session.add(new_channel)
        db.session.commit()
        return new_channel
    except Exception as arror:
        db.session.rollback()
        raise arror


def update_channel(channel_id, **kwargs):
    try:
        channel = Channel.query.filter_by(id=channel_id).one_or_none()
        if channel is None:
            return channel

        channel.title = kwargs.get("title")
        channel.comment_count = (
            kwargs.get("comment_count")
            if kwargs.get("comment_count") is not None
            else 0
        )
        channel.video_count = kwargs.get("video_count")
        channel.url = kwargs.get("img_url")

        db.session.commit()
        return channel
    except Exception as error:
        db.session.rollback()
        raise error


def delete_channel(channel_id):
    try:
        channel = Channel.query.filter_by(id=channel_id).one_or_none()

        if channel is None:
            return channel

        db.session.delete(channel)
        db.session.commit()
        return channel
    except Exception as error:
        db.session.rollback()
        raise error
