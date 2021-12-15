from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from evereview.utils.dto import ChannelDto
from evereview.services import oauth_service, user_service, channel_service

api = ChannelDto.api

parser = reqparse.RequestParser()
parser.add_argument(
    "Authorization",
    location="headers",
    required=True,
    help='"Bearer {access_token}"',
)


@api.route("")
@api.response(200, "Channels Success", ChannelDto.channel_list)
@api.response(400, "Channel Fail(잘못된 요청)", ChannelDto.fail)
@api.response(403, "Channel Fail(권한 없음, 존재하지 않거나 해당 유저의 채널이 아님)", ChannelDto.fail)
class Channels(Resource):
    channel_parser = parser.copy()
    channel_parser.add_argument(
        "channel_id",
        location="args",
        help="channel_id 입력하면 해당 채널 정보, 입력 안하면 유저의 전체 채널 리스트",
    )

    @api.expect(channel_parser)
    @jwt_required()
    def get(self):
        """
        채널들 정보
        """
        user_id = get_jwt_identity()
        user = user_service.get_user_by_id(user_id)
        oauth_token = user.oauth_token

        channel_id = self.channel_parser.parse_args().get("channel_id")

        channels_db = channel_service.get_channels(user_id)
        user_channel_id = list(map(lambda channel: channel.get("id"), channels_db))

        channels_oauth = oauth_service.fetch_user_channels(
            oauth_token, admin=user.admin
        )

        result = []

        for channel in channels_oauth:
            if channel.get("channel_id") in user_channel_id:
                updated_channel = channel_service.update_channel(
                    channel_id=channel.get("channel_id"),
                    user_id=user_id,
                    title=channel.get("title"),
                    comment_count=channel.get("comment_count"),
                    video_count=channel.get("video_count"),
                    channel_url=channel.get("channel_url"),
                    img_url=channel.get("img_url"),
                )
                result.append(updated_channel.to_dict())
            elif channel.get("channel_id") not in user_channel_id:
                new_channel = channel_service.insert_channel(
                    channel_id=channel.get("channel_id"),
                    user_id=user_id,
                    title=channel.get("title"),
                    comment_count=channel.get("comment_count"),
                    video_count=channel.get("video_count"),
                    channel_url=channel.get("channel_url"),
                    img_url=channel.get("img_url"),
                )
                result.append(new_channel.to_dict())

        if channel_id:
            result = list(filter(lambda item: item.get("id") == channel_id, result))
            if len(result) == 0:
                return {
                    "resut": "fail",
                    "message": "존재하지 않거나 해당 유저의 권한이 없는 채널입니다.",
                }, 403

        return {"channel_items": result}, 200
