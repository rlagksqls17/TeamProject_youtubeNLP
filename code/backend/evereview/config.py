import os
from datetime import timedelta

JSON_AS_ASCII = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=14)

SECRET_KEY = os.environ.get("SECRET_KEY")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

DB_HOST = os.environ.get("DB_HOST")
USER = os.environ.get("DB_USER")
PASSWORD = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")
SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{USER}:{PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"
)
