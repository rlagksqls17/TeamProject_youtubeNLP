import os

from sqlalchemy import create_engine


def get_mysql_engine():
    DB_HOST = os.environ.get("DB_HOST")
    USER = os.environ.get("DB_USER")
    PASSWORD = os.environ.get("DB_PASS")
    DB_NAME = os.environ.get("DB_NAME")

    engine = create_engine(
        f"mysql+pymysql://{USER}:{PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
    )

    return engine
