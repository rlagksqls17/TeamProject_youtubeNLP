FROM python:3.8-alpine
COPY . /app
WORKDIR /app

RUN apk add --no-cache build-base libffi-dev
RUN pip3 install -r requirements.txt
