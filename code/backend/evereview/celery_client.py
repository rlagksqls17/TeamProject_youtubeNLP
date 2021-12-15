import os

from celery import Celery
import pymysql


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


def create_celery():
    celery = Celery(
        "evereview", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND
    )

    celery.conf.update(
        task_track_started=True,
        result_expires=86400,  # one day,
        timezone="Asia/Seoul",
    )

    return celery
