import torch
from torch import nn

from classes import data_etl
from classes import classification

import pandas as pd


class BERTClassifier(nn.Module):
    def __init__(self,
                 bert,
                 hidden_size = 768,
                 num_classes=2, ## 클래스 수 조정: 컨텐츠 요구와 피드백으로 나눌거니 2개
                 dr_rate=None,
                 params=None):
        super(BERTClassifier, self).__init__()
        self.bert = bert
        self.dr_rate = dr_rate

        self.classifier = nn.Linear(hidden_size, num_classes)
        if dr_rate:
            self.dropout = nn.Dropout(p=dr_rate)
    
    def gen_attention_mask(self, token_ids, valid_length):
        attention_mask = torch.zeros_like(token_ids)
        for i, v in enumerate(valid_length):
            attention_mask[i][:v] = 1
            return attention_mask.float()
    
    def forward(self, token_ids, valid_length, segment_ids):
        attention_mask = self.gen_attention_mask(token_ids, valid_length)

        _, pooler = self.bert(input_ids = token_ids, token_type_ids = segment_ids.long(), attention_mask = attention_mask.float().to(token_ids.device), return_dict=False)
        if self.dr_rate:
            out = self.dropout(pooler)
            
        return self.classifier(out)




"""data_etl = 데이터 수집 및 전처리 해주는 클래스"""
etl = data_etl.review_etl()

""" classification = 분류 모델 실행 함수"""
kobert = classification.kobert_classification()

"""데이터 수집: ["videoid1", "videoid2"]"""
target_youtube_comments = etl.extract(["hr-aG521SEA"])

"""데이터 변환 : 분류 모델에 들어갈 데이터로"""
input_data = etl.transform(target_youtube_comments)

"""예측"""
predict = kobert.predict(input_data)

predict_df = pd.DataFrame(target_youtube_comments, columns=['textDisplay', 'textOriginal', 'authorDisplayName', 'publishedAt', 'likeCount', 'authorProfileImageUrl'])

predict_df['predict'] = [a[1] for a in predict]
predict_df.to_csv("/datadrive/TeamProject_youtubeNLP/evereview/result/predict1.csv")


