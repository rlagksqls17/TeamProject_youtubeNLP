from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required

from evereview.utils.dto import CommentDto
from evereview.services.comment_service import get_comment, get_comments

api = CommentDto.api

parser = reqparse.RequestParser()
parser.add_argument(
    "Authorization",
    location="headers",
    required=True,
    help='"Bearer {access_token}"',
)


@api.route("/<string:cluster_id>/<string:comment_id>")
@api.doc(params={"cluster_id": "cluster id"})
@api.doc(params={"comment_id": "comment id"})
@api.response(200, "Comment Success", CommentDto.comment)
@api.response(400, "Channel Fail(잘못된 요청)", CommentDto.fail)
@api.response(403, "Channel Fail(권한 없음)", CommentDto.fail)
@api.response(404, "Video Fail(존재하지 않는 댓글)", CommentDto.fail)
class Comment(Resource):
    @api.expect(parser)
    @jwt_required()
    def get(self, cluster_id, comment_id):
        """
        댓글 하나의 정보
        """
        comment = get_comment(cluster_id, comment_id)
        if comment is None:
            return {"result": "fail", "message": "존재하지 않는 리소스입니다."}, 404

        result = comment

        return result, 200


@api.route("/<string:cluster_id>")
@api.doc(params={"cluster_id": "analysis 요청으로 얻은 cluster_id"})
@api.response(200, "Comments Success", CommentDto.comment_list)
@api.response(400, "Channel Fail(잘못된 요청)", CommentDto.fail)
@api.response(403, "Channel Fail(권한 없음)", CommentDto.fail)
@api.response(404, "Video Fail(존재하지 않는 cluster)", CommentDto.fail)
class Comments(Resource):
    """
    클러스터에 해당하는 댓글들
    """

    @api.expect(parser)
    @jwt_required()
    def get(self, cluster_id):
        comments = get_comments(cluster_id)

        if len(comments) == 0:
            return {"result": "fail", "message": "존재하지 않는 리소스입니다."}, 404

        return comments, 200
