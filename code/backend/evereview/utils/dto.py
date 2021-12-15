from flask_restx import Namespace, fields


class OauthDto:
    api = Namespace(name="oauth", description="oauth 인증을 위해 사용하는 api")

    clientinfo = api.model(
        "clientinfo",
        {
            "client_id": fields.String(description="구글 로그인 요청을 위한 client_id"),
            "scopes": fields.List(fields.String, description="google api scope"),
        },
    )


class AuthDto:
    api = Namespace(name="auth", description="evereview auth api")

    success = api.model(
        "success",
        {"result": fields.String(example="success"), "message": fields.String},
    )
    fail = api.model(
        "fail", {"result": fields.String(example="fail"), "message": fields.String}
    )
    signin_fail = api.model(
        "signin_fail",
        {
            "is_member": fields.Boolean(example=False),
            "email": fields.String(description="이메일"),
            "name": fields.String(description="이름"),
            "img_url": fields.String(description="이미지 url"),
        },
    )
    signin_success = api.model(
        "signin_success",
        signin_fail,
        {
            "is_member": fields.Boolean(example=True),
            "access_token": fields.String(description="엑세스 토큰"),
            "nickname": fields.String(description="닉네임"),
            "upload_term": fields.String(description="업로드 주기"),
            "contents_category": fields.String(description="주력 컨텐츠 카테고리"),
        },
    )
    invalide_code = api.model(
        "invalide_authorization_code",
        {
            "error": fields.String(description="error 유형"),
            "error_description": fields.String(description="error 설명"),
        },
    )
    refresh = api.model(
        "refresh_success",
        {"result": fields.String(example="success"), "access_token": fields.String},
    )


class UserDto:
    api = Namespace("user", description="user 리소스 가져오기, 수정하기")

    success = api.model(
        "user",
        {
            "id": fields.Integer,
            "email": fields.String,
            "name": fields.String,
            "nickname": fields.String,
            "upload_term": fields.Integer,
            "contents_category": fields.String,
            "img_url": fields.String,
        },
    )
    fail = api.model(
        "fail", {"result": fields.String(example="fail"), "message": fields.String}
    )


class ChannelDto:
    api = Namespace("channels", description="channel 리소스 가져오기")

    fail = api.model(
        "fail", {"result": fields.String(default="fail"), "message": fields.String}
    )
    channel = api.model(
        "channel",
        {
            "id": fields.String,
            "title": fields.String,
            "comment_count": fields.Integer,
            "video_count": fields.Integer,
            "channel_url": fields.String,
            "img_url": fields.String,
        },
    )
    channel_list = api.model(
        "channel_list", {"channel_items": fields.List(fields.Nested(channel))}
    )


class VideoDto:
    api = Namespace("videos", description="video 리소스 가져오기")

    fail = api.model(
        "fail", {"result": fields.String(default="fail"), "message": fields.String}
    )
    video = api.model(
        "video",
        {
            "id": fields.String,
            "published_at": fields.DateTime,
            "thumbnail_url": fields.String,
            "category_id": fields.Integer,
            "view_count": fields.Integer,
            "like_count": fields.Integer,
            "comment_count": fields.Integer,
        },
    )
    page_info = api.model(
        "page_info", {"totalResults": fields.Integer, "resultsPerPage": fields.Integer}
    )
    video_list = api.model(
        "video_list",
        {
            "video_items": fields.List(fields.Nested(video)),
            "next_page_token": fields.String,
            "prev_page_token": fields.String,
            "page_info": fields.List(fields.Nested(page_info)),
        },
    )


class CommentDto:
    api = Namespace("comments", description="comment 리소스 가져오기")

    fail = api.model(
        "fail", {"result": fields.String(default="fail"), "message": fields.String}
    )
    video_with_comment = api.model(
        "video_with_comment",
        {
            "title": fields.String,
            "view_count": fields.Integer,
        },
    )
    comment = api.model(
        "comment",
        {
            "id": fields.String,
            "author": fields.String,
            "author_img": fields.String,
            "text_display": fields.String,
            "text_original": fields.String,
            "like_count": fields.Integer,
            "published_at": fields.DateTime,
            "video": fields.Nested(video_with_comment),
        },
    )
    comment_list = api.model(
        "comment_list", {"comment_items": fields.List(fields.Nested(comment))}
    )


class AnalysisDto:
    api = Namespace("analysis", description="분석 api")

    fail = api.model(
        "fail", {"result": fields.String(default="fail"), "message": fields.String}
    )
    predict = api.model("predict", {"analisys_id": fields.String})
    analysis = api.model(
        "analysis",
        {
            "id": fields.String,
            "analysis_at": fields.DateTime,
        },
    )
    top_comment = api.model(
        "top_comment",
        {
            "comment_id": fields.String,
            "cluster_id": fields.String,
            "video_id": fields.String,
            "author": fields.String,
            "author_img_url": fields.String,
            "text_display": fields.String,
            "text_original": fields.String,
            "like_count": fields.Integer,
            "published_at": fields.DateTime,
        },
    )
    cluster = api.model(
        "cluster",
        {
            "id": fields.String,
            "top_comment": fields.Nested(top_comment),
            "code": fields.String,
            "code_description": fields.String,
            "count": fields.Integer,
            "like_count": fields.Integer,
        },
    )
    result = api.model(
        "result",
        {
            "state": fields.String,
            "analisys": fields.Nested(analysis),
            "clusters": fields.List(fields.Nested(cluster)),
        },
    )
