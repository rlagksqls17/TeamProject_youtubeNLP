import torch
from torch import nn

from classes import data_etl
from classes import classification
from classes import clustering

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




# data_etl = 데이터 수집 및 전처리 해주는 클래스
etl = data_etl.review_etl()

# classification = 분류 모델 실행 함수
kobert = classification.kobert_classification()


"""
sample data 

1. 영상별 수집 : video_id=['f0ZAgF7YvlI', '8vAouplPQsc']
2. 댓글 기간별 수집 : channel_id="UChxh4uh0d3OOeRhm-5pv6bA", day_start=20211101, day_end=20211112
"""
target_youtube_comments = etl.extract(video_id=['t9E7Uow8g90'])
# target_youtube_comments = etl.extract(channel_id="UCIG4gr_wIy5CIlcFciUbIQw", day_start=20211101, day_end=20211208)

# 데이터 변환 : 분류 모델에 들어갈 데이터로
input_data = etl.transform(target_youtube_comments)

# 예측
predict = kobert.predict(input_data)

# 분류 예측 결과 df 생성
predict_df = pd.DataFrame(target_youtube_comments, columns=['authorDisplayName', 'authorProfileImageUrl', 'textDisplay', 'textOriginal', 'likeCount', 'publishedAt'])
predict_df['predict'] = [a[1] for a in predict]
predict_df.to_csv("./result/predict.csv")

# predict_df의 'textOriginal' 댓글 데이터 전처리 후 임베딩
preprocessed_tmp = clustering.preprocess_comments(predict_df)
embedded_tmp = clustering.embedding(preprocessed_tmp)

# 임베딩된 데이터를 긍, 부정 피드백, 모든 피드백, 컨텐츠 요구 df로 나눔
# 일부 임베드 데이터는 nan으로 표시되어 에러가 발생하고 있어 dropna() 처리 하였음
requests_df = embedded_tmp[embedded_tmp.predict=="contents"].dropna()
goodFeedback_df = embedded_tmp[embedded_tmp.predict=="good_feedback"].dropna()
badFeedback_df = embedded_tmp[embedded_tmp.predict=="bad_feedback"].dropna()
allFeedback_df = pd.concat([goodFeedback_df, badFeedback_df])

# 각 용도에 맞게 분류된 df를 dbscan 이용해 클러스터링
request_dbscan = clustering.proceed_dbscan(requests_df, eps=4.75)
goodFeedback_dbscan = clustering.proceed_dbscan(goodFeedback_df, eps=4.75)
badFeedback_dbscan = clustering.proceed_dbscan(badFeedback_df, eps=4.75)
allFeedback_dbscan = clustering.proceed_dbscan(allFeedback_df, eps=4.75)

# dbscan으로 군집화되면 이 결과는 정수로 나오는데, 정수가 하나의 군집 이름이라고 생각하면 된다.
# 이 정수를 오름차순 정렬하여 군집화 결과를 다음 3개의 변수에 저장한다.
request_well = request_dbscan.sort_values(by=['dbscanned'], ascending=True).iloc[:, [0, 1, 2, 3, 4, 5, -1]]
goodFeedback_well = goodFeedback_dbscan.sort_values(by=['dbscanned'], ascending=True).iloc[:, [0, 1, 2, 3, 4, 5, -1]]
badFeedback_well = badFeedback_dbscan.sort_values(by=['dbscanned'], ascending=True).iloc[:, [0, 1, 2, 3, 4, 5, -1]]
allFeedback_well = allFeedback_dbscan.sort_values(by=['dbscanned'], ascending=True).iloc[:, [0, 1, 2, 3, 4, 5, -1]]

request_well.to_csv("./result/request_well.csv")
goodFeedback_well.to_csv("./result/goodFeedback_well.csv")
badFeedback_well.to_csv("./result/badFeedback_well.csv")
allFeedback_well.to_csv("./result/allFeedback_well.csv")
