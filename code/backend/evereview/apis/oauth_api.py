from flask_restx import Resource

from evereview.utils.dto import OauthDto
from evereview.services.oauth_service import CLIENT_ID, SCOPE


api = OauthDto.api


@api.route("/clientinfo")
@api.response(200, "SUCCESS", OauthDto.clientinfo)
class ClientInfo(Resource):
    def get(self):
        return {"client_id": CLIENT_ID, "scopes": SCOPE}
