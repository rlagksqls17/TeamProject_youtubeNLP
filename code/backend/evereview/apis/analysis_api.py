from datetime import datetime

from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from celery import states

from evereview.utils.dto import AnalysisDto
from evereview.services.channel_service import get_channel
from evereview.services.video_service import get_videos
from evereview.services.analysis_service import get_analysis
from evereview.services.cluster_service import get_clusters
from evereview.services.comment_service import get_comment
from evereview.celery_client import create_celery
from evereview.db_connect import db

api = AnalysisDto.api
celery = create_celery()

parser = reqparse.RequestParser()
parser.add_argument(
    "Authorization",
    location="headers",
    required=True,
    help='"Bearer {access_token}"',
)


@api.route("/predict")
@api.response(200, "predict", AnalysisDto.predict)
@api.response(400, "predict Fail(잘못된 요청)", AnalysisDto.fail)
@api.response(403, "predict Fail(토큰 만료)", AnalysisDto.fail)
class Predict(Resource):
    predict_parser = parser.copy()
    predict_parser.add_argument(
        "channel_id",
        type=str,
        location="form",
        help="채널 id",
    )
    predict_parser.add_argument(
        "video_list",
        type=str,
        action="split",
        location="form",
        help="video_id 리스트",
    )
    predict_parser.add_argument(
        "day_start",
        type=str,
        location="form",
        help="시작 날짜 : YYYY-MM-dd",
    )
    predict_parser.add_argument(
        "day_end",
        type=str,
        location="form",
        help="마지막 날짜: YYYY-MM-dd",
    )

    @api.expect(predict_parser)
    @jwt_required()
    def post(self):
        """
        분석 요청하기
            1. day_start < day_end
                - 날짜 포맷 정하기
                - 입력, worker에서 날짜 포맷 통일
                - datetime 변환 후 비교 연산 후 validate
        """
        args = self.predict_parser.parse_args()
        user_id = get_jwt_identity()
        channel_id = args.get("channel_id")
        videos = args.get("video_list")
        day_start = args.get("day_start")
        day_end = args.get("day_end")

        channel = get_channel(channel_id)
        if channel is None:
            return {"result": "fail", "message": "없는 채널입니다."}, 404

        videos_db = get_videos(channel_id)
        videos_db = set(map(lambda item: item.get("id"), videos_db))
        for video in videos:
            if video not in videos_db:
                return {"result": "fail", "message": f"없는 영상입니다.({video})"}, 404

        # day validate startdate < enddate
        if day_start:
            day_start = datetime.strptime(day_start, "%Y-%m-%d")
        if day_end:
            day_end = datetime.strptime(day_end, "%Y-%m-%d")

        if videos and (day_start or day_end):
            return {"result": "fail", "message": "비디오랑 날짜 둘 중 한가지만 입력해주세요"}, 400
        elif not (videos or (day_start and day_end)):
            return {"result": "fail", "message": "비디오나 날짜를 입력해주세요"}, 400

        result = celery.send_task(
            "evereview.predict",
            args=(user_id, channel_id),
            kwargs={
                "videos": videos,
                "day_start": day_start,
                "day_end": day_end,
            },
        )

        return {"analysis_id": result.id}


@api.route("/result/<string:analysis_id>")
@api.doc(params={"analysis_id": "analysis_id"})
@api.response(200, "predict result", AnalysisDto.result)
@api.response(400, "predict result Fail(잘못된 요청)", AnalysisDto.fail)
@api.response(403, "predict result Fail(토큰 만료)", AnalysisDto.fail)
@api.response(404, "predict result Fail(없는 리소스)", AnalysisDto.fail)
class PredictResult(Resource):
    @api.expect(parser)
    @jwt_required()
    def get(self, analysis_id):
        """
        분석 결과 요청
        -- state 설명 --
        STARTED (task has been started)
        RETRY (task is being retried)
        PENDING (waiting for execution or unknown task id)
        ㄴ 다시 시도
        REVOKED (task has been revoked)
        FAILURE (task execution resulted in exception)
        ㄴ 실패
        SUCCESS (task executed successfully)
        ㄴ 성공
        """
        task_result = celery.AsyncResult(analysis_id)
        task_result.ready()

        analysis = get_analysis(analysis_id)

        if task_result.state == states.SUCCESS or analysis is not None:
            analysis = analysis.to_dict()
            clusters = get_clusters(analysis_id)

            clusters_list = []
            for cluster in clusters:
                top_comment = get_comment(cluster.id, cluster.top_comment)
                del top_comment["cluster_id"]

                clusters_list.append(
                    {
                        "id": cluster.id,
                        "top_comment": top_comment,
                        "code": cluster.code,
                        "code_description": cluster.description,
                        "count": cluster.count,
                        "like_count": cluster.like_count,
                    }
                )

            result = {"state": task_result.state}
            result["analysis"] = {
                "id": analysis.get("id"),
                "analysis_at": analysis.get("analysis_at"),
            }
            result["clusters"] = clusters_list

            return result, 200
        elif task_result.state == states.PENDING:
            analysis = db.engine.execute(
                "select task_id from celery_taskmeta where task_id=%s", (analysis_id)
            )
            analysis = [row[0] for row in analysis]
            if not analysis:
                return {"result": "fail", "message": "존재하지 않는 리소스입니다."}, 404

            return {"state": task_result.state, "analysis": None, "clusters": None}, 200

        else:
            return {"state": task_result.state, "analysis": None, "clusters": None}, 200
