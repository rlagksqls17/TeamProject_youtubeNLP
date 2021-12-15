#-*- coding:utf-8 -*-
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from evereview.utils.dto import UserDto
from evereview.services.user_service import get_user_by_id, update_user

api = UserDto.api

parser = reqparse.RequestParser()
parser.add_argument(
    "Authorization",
    location="headers",
    required=True,
    help='"Bearer {access_token}"',
)


@api.route("")
@api.response(200, "Update User Success", UserDto.success)
@api.response(400, "Refresh Fail(잘못된 요청, 파라미터 누락)", UserDto.fail)
@api.response(403, "Refresh Fail(토큰 만료)", UserDto.fail)
@api.response(404, "Refresh Fail(존재하지 않는 회원)", UserDto.fail)
class User(Resource):
    patch_parser = parser.copy()
    patch_parser.add_argument(
        "nickname", type=str, location="form", required=True, help="변경할 닉네임(별명)"
    )
    patch_parser.add_argument(
        "upload_term", type=int, location="form", required=True, help="변경할 영상업로드 주기"
    )
    patch_parser.add_argument(
        "contents_category",
        type=str,
        required=True,
        action="split",
        location="form",
        help="변경할 주력 컨텐츠 카테고리",
    )

    @api.expect(parser)
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = get_user_by_id(user_id)
        result = user.to_dict()

        return result, 200

    @api.expect(patch_parser)
    @jwt_required()
    def patch(self):
        user_id = get_jwt_identity()

        args = self.patch_parser.parse_args()

        nickname = args.get("nickname")
        upload_term = args.get("upload_term")
        contents_category = args.get("contents_category")

        user = update_user(
            user_id=user_id,
            nickname=nickname,
            upload_term=upload_term,
            contents_category=contents_category,
        )
        result = user.to_dict()

        return result, 200
