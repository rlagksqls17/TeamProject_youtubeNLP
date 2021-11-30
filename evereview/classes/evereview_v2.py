import torch
from torch import nn

import numpy as np
import pandas as pd
import gluonnlp as nlp

from googleapiclient.discovery import build  
from kobert.pytorch_kobert import get_kobert_model
from kobert_tokenizer import KoBERTTokenizer



class review_etl:
    def extract(self, video_id):
        """
        <Parmeter> 
            - video_id 
            설명 : 유튜브 비디오 영상의 id 리스트 입력
            형식 : 리스트 (ex 1: ['videoid1']) (ex 2: ['videoid1', 'videoid2'])
            
        <return>
            - comments 
            설명 : 해당 영상에 달린 모든 최신 댓글 리스트 출력
            형식 : 중첩 리스트 (ex : [댓글 리스트1, 댓글 리스트2, 댓글 리스트3])
            
            <댓글 리스트 요소 설명>
            'textDisplay' : 댓글의 html 코드, 텍스트  
            'textOriginal' : 댓글의 텍스트
            'authorDisplayName' : 댓글 작성자 닉네임
            'publishedAt' : 댓글 최초 작성 일자  
            'likeCount' : 댓글의 좋아요 수  
            'authorProfileImageUrl' : 댓글 작성자의 썸네일 Url  
        """

        try:
            comments = list()  
            api_key = "AIzaSyCrzeLdyyZ8k6oBUXm2AeyX20GYV83novM"
            api_obj = build('youtube', 'v3', developerKey=api_key)
            
            for video in video_id:
                response = api_obj.commentThreads().list(part='snippet,replies', videoId=video, maxResults=100).execute() # execute로 html코드 풀어줌
                
                # while문 이용하여 각 영상에 대한 댓글을 페이지네이션 하여 모두 불러온다.
                while response:
                    for item in response['items']:
                        comment = item['snippet']['topLevelComment']['snippet']

                        # 리스트 요소 설명 상기 함수 주석 참고
                        comments.append([comment['textDisplay'], comment['textOriginal'], comment['authorDisplayName'], 
                                            comment['publishedAt'], comment['likeCount'], comment['authorProfileImageUrl']])
                    
                    # 댓글의 끝 페이지 요청에서 다음페이지로 가는 토큰이 있을 경우 그 토큰을 다음 api 요청으로 함
                    if 'nextPageToken' in response:
                        response = api_obj.commentThreads().list(part='snippet,replies', 
                                                                    videoId=video, 
                                                                    pageToken=response['nextPageToken'], 
                                                                    maxResults=100).execute()
                    else:
                        break

            return comments
        
        # 올바르지 않은 video_id가 입력되었을 경우
        except:
            raise ValueError("올바르지 않은 video_id 입니다. 확인 후 다시 입력주세요.")
        

    def transform(self, data=None):
        """
        <parameter>
        - data : 변환을 수행할 데이터
            default : 파라미터 미 지정 시 None으로 지정
            data : [[comment, label], [comment, label], ...[comment, label]] 형식으로 input 되어야 함   
        """
        if data == None:
            raise ValueError("변환시킬 데이터를 넣어주세요. ex: transform(use_case, data)")
        
        else:
            comment_lists = []
            for comment in data:
                comment_lists.append(comment[1])

            return comment_lists


class kobert_classification:
    def __init__(self):
        self.device = torch.device("cuda:0")
        self.tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
        self.tok = self.tokenizer.tokenize
        self.bertmodel, self.vocab = get_kobert_model('skt/kobert-base-v1', self.tokenizer.vocab_file)
        
        self.batch_size = 64
        self.max_len = 64 


    def predict(self, input_data):

        predict_data = []  # return
        count = 0  # 실행 확인용
        
        # 컨텐츠 피드백 분류 모델, 긍부정 분류모델 불러옴
        feedback_classifier = torch.load('./feedback_classifier')
        goodbad_classifier = torch.load('./goodbad_classifier')

        for idx, i in enumerate(input_data):
            print(count)
            count += 1
            i_result = []
            i_result.append(i)

            # 모델에 들어갈 데이터
            data = [i, '0']
            dataset_feedback = [data]
            feedback_test = BERTDataset(dataset_feedback, 0, 1, self.tok, self.vocab, self.max_len, True, False)
            feedback_dataloader = torch.utils.data.DataLoader(feedback_test, batch_size=self.batch_size, num_workers=5)
            feedback_classifier.eval()

            for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(feedback_dataloader):
                
                # 모델 파라미터
                feedback_token = token_ids.long().to(self.device)
                feedback_segment = segment_ids.long().to(self.device)
                feedback_valid = valid_length
                feedback_label = label.long().to(self.device)

                # 모델 실행
                out = feedback_classifier(feedback_token, feedback_valid, feedback_segment)

                for index in out:
                    logits = index
                    feedback_logits = logits.detach().cpu().numpy()

                    # 예측 결과가 0일 경우 피드백으로 간주하고 여기서 다시 긍부정 분류함
                    if np.argmax(feedback_logits) == 0:

                        # 모델에 들어갈 데이터
                        data = [i, '0']
                        dataset_goodbad = [data]
                        goodbad_test = BERTDataset(dataset_goodbad, 0, 1, self.tok, self.vocab, self.max_len, True, False)
                        goodbad_dataloader = torch.utils.data.DataLoader(goodbad_test, batch_size=self.batch_size, num_workers=5)
                        goodbad_classifier.eval()

                        
                        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(goodbad_dataloader):
                            
                            # 모델 파라미터
                            goodbad_token = token_ids.long().to(self.device)
                            goodbad_segment = segment_ids.long().to(self.device)
                            goodbad_valid = valid_length
                            goodbad_label = label.long().to(self.device)
                            
                            # 모델 실행
                            out_goodbad = goodbad_classifier(goodbad_token, goodbad_valid, goodbad_segment)

                            for index in out_goodbad:
                                logits = index
                                goodbad_logits = logits.detach().cpu().numpy()
                                if np.argmax(goodbad_logits) == 0:
                                    print("부정")
                                    i_result.append("bad_feedback")
                                elif np.argmax(goodbad_logits) == 1:
                                    print("긍정")
                                    i_result.append("good_feedback")

                    elif np.argmax(feedback_logits) == 1:
                        print("콘텐츠")
                        i_result.append("contents")

            predict_data.append(i_result)

        return predict_data


class BERTDataset:
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, vocab, max_len, pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, vocab=vocab, pad=pad, pair=pair)
        
        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]
    
    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))
    
    def __len__(self):
        return (len(self.labels))


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



# 객체 생성
etl = review_etl() # 데이터 전처리
kobert = kobert_classification() # kobert 모델

# 데이터 수집
target_youtube_comments = etl.extract(["ibydOspB5y0"])

# 데이터 변환
input_data = etl.transform(data=target_youtube_comments)

# 변환된 데이터 예측
predict = kobert.predict(input_data)

# 예측이 되고 나면 예측결과를 기존의 수집 정보 (작성자 닉네임, 좋아요 수 등)에 추가
predict_df = pd.DataFrame(target_youtube_comments, columns=['textDisplay', 'textOriginal', 'authorDisplayName', 'publishedAt', 'likeCount', 'authorProfileImageUrl'])
predict_df['predict'] = [a[1] for a in predict]

predict_df.to_csv("./predict.csv")


