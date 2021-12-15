## 실행 순서

### development 환경

- export FLASK_APP=evereview.app 명령으로 환경변수 설정
- requirements.txt 설치
- config.py 비어있는 데이터베이스 정보 입력
- backend 폴더에서 아래 명령어 실행
  - flask db init
  - flask db migrate
  - flask db upgrade
  - flask run

## 라이브러리

- flask
- flask-cors
- flask-jwt-extended
- flask-migrate
- flask-restx
- flask-sqlalchemy

## API 문서

- http://tanficial-dev.kro.kr:5000/api/

## 데이터베이스 ERD

![evereview_erd_v2](/uploads/e11a751a158b118724966f7c63d48cd7/evereview_erd_v2.JPG)

## oauth 인증 절차

![oauth_sequence](/uploads/a5785721e24df9662cdd48b23e9c7848/oauth_sequence.png)
