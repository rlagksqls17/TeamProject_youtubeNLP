from datetime import datetime

from flask_restx import Resource, reqparse
import flask_jwt_extended as flask_jwt

from evereview.utils.dto import AuthDto
from evereview.services import oauth_service, user_service


api = AuthDto.api

parser = reqparse.RequestParser()
parser.add_argument(
    "Authorization",
    location="headers",
    required=True,
    help='"Bearer {access_token}"',
)


@api.route("/signin")
@api.response(200, "Signin Success", AuthDto.signin_success)
@api.response(400, "Signin Fail(잘못된 authorization 코드)", AuthDto.invalide_code)
@api.response(404, "Signin Fail(회원이 아님)", AuthDto.signin_fail)
class Signin(Resource):
    signin_parser = reqparse.RequestParser()
    signin_parser.add_argument(
        "code",
        type=str,
        location="form",
        required=True,
        help="google login을 통해 얻은 authorization code",
    )

    @api.expect(signin_parser)
    def post(self):
        code = self.signin_parser.parse_args().get("code")
        oauth_result = oauth_service.authorization(code)
        if "oauth_token" not in oauth_result.keys():
            return oauth_result, 400

        oauth_token = oauth_result.get("oauth_token")
        user_email = oauth_result.get("user_email")
        user_name = oauth_result.get("user_name")
        user_img = oauth_result.get("user_img")

        user = user_service.get_user_by_email(user_email)
        if user is None:
            return {
                "is_member": False,
                "email": user_email,
                "name": user_name,
                "img_url": user_img,
            }, 404

        user = user_service.update_user_googleinfo(
            user_id=user.id, name=user_name, img_url=user_img
        )

        access_token = flask_jwt.create_access_token(identity=user.id)
        refresh_token = flask_jwt.create_refresh_token(identity=user.id)
        user_service.update_token(
            user_id=user.id,
            oauth_token=oauth_token,
            access_token=access_token,
            refresh_token=refresh_token,
        )

        result = user.to_dict()
        result["is_member"] = True
        result["access_token"] = access_token

        return result, 200


@api.route("/signup")
@api.response(200, "Signup Success", AuthDto.success)
@api.response(409, "Signup Fail(이미 가입된 이메일)", AuthDto.fail)
class Signup(Resource):
    signup_parser = reqparse.RequestParser()
    signup_parser.add_argument(
        "email", type=str, location="form", required=True, help="email"
    )
    signup_parser.add_argument(
        "name", type=str, location="form", required=True, help="이름"
    )
    signup_parser.add_argument(
        "nickname", type=str, location="form", required=True, help="닉네임(별명)"
    )
    signup_parser.add_argument(
        "img_url", type=str, location="form", required=True, help="프로필 이미지 url"
    )
    signup_parser.add_argument(
        "upload_term", type=int, location="form", required=True, help="업로드 주기"
    )
    signup_parser.add_argument(
        "contents_category",
        type=str,
        action="split",
        location="form",
        required=True,
        help="주력 컨텐츠 카테고리",
    )

    @api.expect(signup_parser)
    def post(self):
        form_data = self.signup_parser.parse_args()
        email = form_data.get("email")
        name = form_data.get("name")
        nickname = form_data.get("nickname")
        img_url = form_data.get("img_url")
        upload_term = form_data.get("upload_term")
        contents_category = form_data.get("contents_category")

        user = user_service.get_user_by_email(email)
        if user is not None:
            return {"result": "fail", "message": "이미 가입된 이메일입니다."}, 409

        user_service.insert_user(
            email=email,
            name=name,
            nickname=nickname,
            img_url=img_url,
            upload_term=upload_term,
            contents_category=contents_category,
        )

        return {"result": "success"}, 200


@api.route("/signout")
@api.response(200, "Signout Success", AuthDto.success)
@api.response(403, "Signout Fail(토큰 만료)", AuthDto.fail)
@api.response(400, "Signout Fail(잘못된 요청)", AuthDto.fail)
class Signout(Resource):
    @api.expect(parser)
    @flask_jwt.jwt_required()
    def get(self):
        user_id = flask_jwt.get_jwt_identity()
        user_service.update_token(
            user_id=user_id, oauth_token=None, access_token=None, refresh_token=None
        )
        return {"result": "success", "message": "로그아웃 성공"}, 200


@api.route("/refresh")
@api.response(200, "Refresh Success", AuthDto.success)
@api.response(404, "Refresh Fail(존재하지 않는 회원)", AuthDto.fail)
@api.response(403, "Refresh Fail(토큰 만료)", AuthDto.fail)
@api.response(400, "Refresh Fail(잘못된 요청)", AuthDto.fail)
class Refresh(Resource):
    @api.expect(parser)
    @flask_jwt.jwt_required()
    def get(self):
        user_id = flask_jwt.get_jwt_identity()

        user = user_service.get_user_by_id(user_id=user_id)
        if user is None:
            return {"result": "fail", "message": "존재하지 않는 회원입니다."}, 404

        access_token = user.access_token
        refresh_token = user.refresh_token
        if not user.refresh_token:
            return {"result": "fail", "message": "다시 로그인 해주세요"}, 403

        try:
            decoded_access_token = flask_jwt.decode_token(
                access_token, allow_expired=True
            )
            if flask_jwt.get_jwt().get("exp") != decoded_access_token.get("exp"):
                return {"result": "fail", "message": "다시 로그인 해주세요"}, 403

            decoded_refresh_token = flask_jwt.decode_token(
                refresh_token, allow_expired=True
            )
            if decoded_refresh_token.get("exp") < datetime.now():
                return {"result": "fail", "message": "다시 로그인 해주세요"}, 403

            new_access_token = flask_jwt.create_access_token(
                identity=decoded_refresh_token.get("sub")
            )
            user_service.update_token(
                user_id=user.id,
                oauth_token=user.oauth_token,
                access_token=new_access_token,
                refresh_token=user.refresh_token,
            )
            return {"result": "success", "access_token": new_access_token}, 200
        except Exception as error:
            raise error
