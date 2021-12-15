from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required

from evereview.utils.dto import VideoDto
from evereview.services import oauth_service, video_service, channel_service


api = VideoDto.api

parser = reqparse.RequestParser()
parser.add_argument(
    "Authorization",
    location="headers",
    required=True,
    help='"Bearer {access_token}"',
)


@api.route("/<string:video_id>")
@api.doc(params={"video_id": "video_id"})
@api.response(200, "Video Success", VideoDto.video)
@api.response(400, "Channel Fail(잘못된 요청)", VideoDto.fail)
@api.response(403, "Channel Fail(권한 없음)", VideoDto.fail)
@api.response(404, "Video Fail(존재하지 않는 영상)", VideoDto.fail)
class Video(Resource):
    @api.expect(parser)
    @jwt_required()
    def get(self, video_id):
        """
        영상 하나의 정보
        """
        video = video_service.get_video(video_id)
        if video is None:
            return {"result": "fail", "message": "존재하지 않는 리소스입니다."}, 404

        result = video.to_dict()
        return result, 200


@api.route("")
@api.response(200, "Video Success", VideoDto.video_list)
@api.response(400, "Channel Fail(잘못된 요청)", VideoDto.fail)
@api.response(403, "Channel Fail(권한 없음)", VideoDto.fail)
@api.response(404, "Video Fail(존재하지 않는 채널)", VideoDto.fail)
class SearchVideos(Resource):
    search_parser = parser.copy()
    search_parser.add_argument(
        "channel_id",
        location="args",
        required=True,
        help="channel_id",
    )
    search_parser.add_argument(
        "query",
        location="args",
        help="검색어, 검색 결과는 관련도순, 검색어 없으면 전체 영상 최신순",
    )
    search_parser.add_argument(
        "page_token",
        location="args",
        help="페이지 토큰, 페이지 토큰 없으면 첫번째 페이지 리턴",
    )

    @api.expect(search_parser)
    @jwt_required()
    def get(self):
        """
        여러 영상 정보
        """
        args = self.search_parser.parse_args()
        channel_id = args.get("channel_id")
        query = args.get("query").strip() if args.get("query") else None
        page = args.get("page_token")

        channel = channel_service.get_channel(channel_id)
        if channel is None:
            return {"result": "fail", "message": "존재하지 않는 채널입니다"}, 404

        if query:
            (
                new_videos,
                page_info,
                next_page_token,
                prev_page_token,
            ) = oauth_service.search_videos(query, channel_id, page)
        else:
            (
                new_videos,
                page_info,
                next_page_token,
                prev_page_token,
            ) = oauth_service.fetch_videos(channel_id, page)

        videos = video_service.get_videos(channel_id)
        videos_id = set(map(lambda video: video.get("id"), videos))

        video_itmes = []
        for video in new_videos:
            video_id = video.get("id")
            if video_id in videos_id:
                item = video_service.update_video(
                    video_id=video_id,
                    title=video.get("title"),
                    thumbnail_url=video.get("thumbnail_url"),
                    category_id=video.get("category_id"),
                    view_count=video.get("view_count"),
                    like_count=video.get("like_count"),
                    comment_count=video.get("comment_count"),
                )
            else:
                item = video_service.insert_video(
                    video_id=video_id,
                    channel_id=video.get("channel_id"),
                    title=video.get("title"),
                    published_at=video.get("published_at"),
                    thumbnail_url=video.get("thumbnail_url"),
                    category_id=video.get("category_id"),
                    view_count=video.get("view_count"),
                    like_count=video.get("like_count"),
                    comment_count=video.get("comment_count"),
                )
            video_itmes.append(item.to_dict())

        result = {}
        result["video_items"] = video_itmes
        result["page_info"] = page_info
        result["next_page_token"] = next_page_token
        result["prev_page_token"] = prev_page_token

        return result, 200
