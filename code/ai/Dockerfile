FROM nvidia/cuda:11.2.2-cudnn8-runtime-ubuntu20.04

RUN apt update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y git
RUN pip3 install pandas
RUN pip3 install celery
RUN pip3 install torch
RUN pip3 install tensorflow
RUN pip3 install google-api-python-client
RUN pip3 install sqlalchemy
RUN pip3 install pymysql
RUN pip3 install git+https://github.com/SKTBrain/KoBERT.git@master
RUN pip3 install 'git+https://github.com/SKTBrain/KoBERT.git#egg=kobert_tokenizer&subdirectory=kobert_hf'
