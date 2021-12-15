from flask import Flask, Blueprint
from flask_cors import CORS
from flask_migrate import Migrate
import flask_jwt_extended
from flask_restx import Api
import jwt

from evereview import config
from evereview.db_connect import db

from evereview.apis.oauth_api import api as oauth_namespace
from evereview.apis.auth_api import api as auth_namespace
from evereview.apis.user_api import api as user_namespace
from evereview.apis.channel_api import api as channel_namespace
from evereview.apis.video_api import api as video_namespace
from evereview.apis.comment_api import api as comment_namespace
from evereview.apis.analysis_api import api as analysis_namespace


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, supports_credentials=True)
    flask_jwt_extended.JWTManager(app)

    db.init_app(app)
    Migrate().init_app(app, db)

    @app.route("/")
    def landing():
        return "hello evereview"

    restx_bp = Blueprint("api", __name__, url_prefix="/api")
    restx = Api(restx_bp)
    restx.add_namespace(oauth_namespace)
    restx.add_namespace(auth_namespace)
    restx.add_namespace(user_namespace)
    restx.add_namespace(channel_namespace)
    restx.add_namespace(video_namespace)
    restx.add_namespace(comment_namespace)
    restx.add_namespace(analysis_namespace)

    @restx.errorhandler
    def default_error_handler(error):
        if isinstance(error, jwt.exceptions.ExpiredSignatureError):
            return {"result": "fail", "message": "토큰이 만료되었습니다."}, 403
        elif isinstance(error, jwt.exceptions.DecodeError):
            return {"result": "fail", "message": "올바른 토큰이 아닙니다."}, 400
        elif isinstance(error, flask_jwt_extended.exceptions.NoAuthorizationError):
            return {"result": "fail", "message": "Bearer 타입이 아닙니다."}, 400

        raise error

    app.register_blueprint(restx_bp)

    return app


application = create_app()

if __name__ == "__main__":

    HOST = "0.0.0.0"
    PORT = 5000
    application.run(host=HOST, port=PORT)
