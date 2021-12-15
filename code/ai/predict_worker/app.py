import os
from datetime import datetime
import random
import uuid

from celery import Celery
import pandas as pd
import numpy as np
import pymysql

from predict_worker.youtube.data_etl import review_etl
from predict_worker.db_connect import get_mysql_engine
from predict_worker.utils.exceptions import VideosDateException

pymysql.install_as_MySQLdb()

RABBITMQ_USER = os.environ.get("RABBITMQ_DEFAULT_USER")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_DEFAULT_PASS")
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")

CELERY_BROKER_URL = f"pyamqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}//"
CELERY_RESULT_BACKEND = (
    f"db+mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
)

app = Celery("evereview", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

app.conf.update(
    task_track_started=True,
    result_expires=86400,  # one day,
    timezone="Asia/Seoul",
)


@app.task(name="evereview.predict", bind=True)
def predict(self, user_id, channel_id, **kwargs):
    videos = kwargs.get("videos")
    day_start = kwargs.get("day_start")
    day_end = kwargs.get("day_end")

    review_extracter = review_etl()

    if videos and day_start and day_end:
        # 영상별 + 기간별
        # 실패(임시)
        raise VideosDateException()
    elif videos:
        # 영상별
        comment_list = review_extracter.extract(video_id=videos)
    elif day_start and day_end:
        # 기간별
        comment_list = review_extracter.extract(
            channel_id=channel_id, day_start=day_start, day_end=day_end
        )
    else:
        # 실패
        raise VideosDateException()

    ## extract raw text
    # textOriginal 리스트 or df 생성

    ## 예측
    """
    피드백 or 컨텐츠 분류
        피드백
            - 긍정 / 부정 분류
            - clustering
        컨텐츠
            - clustering
            - cluster 카테고리 별로 분류

    ### 댓글에 랜덤 ai 결과 넣기(mock)
    ## 피드백/컨텐츠
    ## 피드백 긍,부정
    ## 피드백 클러스터링
    ## 컨텐츠 클러스터링
    ## 컨텐츠 분류
    """
    ## 임시로 분류, 군집화, 클러스터 정보 생성
    feedback_or_content = np.random.randint(0, 2, comment_list.shape[0])
    feedback_cluster_list = [
        (uuid.uuid4().hex[:8], "P" if random.randrange(0, 2) == 1 else "N")
        for _ in range(10)
    ]
    content_cluster_list = [uuid.uuid4().hex[:8] for _ in range(10)]
    cluster_id = []
    code = []
    for fc in feedback_or_content:
        if fc == 0:
            cluster = feedback_cluster_list[
                random.randrange(len(feedback_cluster_list))
            ]
            cluster_id.append(cluster[0])
            code.append("F" + cluster[1])
        elif fc == 1:
            cluster = content_cluster_list[random.randrange(len(content_cluster_list))]
            cluster_id.append(cluster)
            code.append("C")
    comment_list["cluster_id"] = cluster_id
    comment_list["code"] = code

    ## db에 저장
    """
    analysis 테이블 저장
    ## id, user_id, analysis_at

    cluster 테이블 저장
    ## id, analysis_id, code, top_comment, count, like_count
    ## 요부분도 df.to_sql로 저장

    comment 테이블 저장
    ## +(id, video_id 추가) + cluster_id
    ## 요부분은 df.to_sql로 저장
    """
    # analysis
    analysis_id = self.request.id
    analysis_at = datetime.now()

    # cluster
    ## 집계
    top_comment = comment_list.sort_values(
        "like_count", ascending=False
    ).drop_duplicates("cluster_id")[["cluster_id", "id", "code"]]
    cluster = comment_list.groupby(["cluster_id"])
    cluster = pd.DataFrame(
        {"like_count": cluster["like_count"].sum(), "count": cluster["id"].count()}
    )
    cluster = pd.merge(
        cluster, top_comment, left_on="cluster_id", right_on="cluster_id", how="inner"
    )
    cluster.rename(columns={"id": "top_comment", "cluster_id": "id"}, inplace=True)
    cluster["analysis_id"] = analysis_id
    cluster.set_index("id")

    # comment
    ## db 저장을 위해 code 칼럼 삭제
    comment_list.drop("code", axis=1, inplace=True)

    # mysql db에 결과 저장
    engine = get_mysql_engine()
    with engine.begin() as connection:
        connection.execute(
            "INSERT INTO analysis(id, user_id, analysis_at) VALUES(%s, %s, %s)",
            (analysis_id, user_id, analysis_at),
        )
        cluster.to_sql("cluster", con=connection, if_exists="append", index=False)
        comment_list.to_sql("comment", con=connection, if_exists="append", index=False)

    ## 결과 summary 리턴
    result = {}
    result["analysis"] = {"id": analysis_id, "analysis_at": analysis_at}
    result["cluster"] = cluster.to_dict("records")
    return result
