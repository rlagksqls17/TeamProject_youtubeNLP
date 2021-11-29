import pandas as pd  
import numpy as np  
from googleapiclient.discovery import build  

import torch  
from torch import nn 
import torch.nn.functional as F  
import torch.optim as optim  
from torch.utils.data import Dataset, DataLoader  
import gluonnlp as nlp
from tqdm import tqdm, tqdm_notebook  

from kobert.pytorch_kobert import get_kobert_model
from kobert_tokenizer import KoBERTTokenizer
  
from transformers import BertModel  
from transformers import AdamW  
from transformers.optimization import get_cosine_schedule_with_warmup



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
        

    def transform(self, use_case, data=None):
        """
        <parameter>
        - use_case : 함수의 사용 목적에 따라 데이터를 다르게 변환해 줌
            classification : 분류 모델에게 예측을 요청할 데이터를 제작
                ex) transform("classification")

            training : 분류 모델에 학습시킬 데이터 전처리
                ex) transform("training", data)

        - data : 변환을 수행할 데이터
            default : 파라미터 미 지정 시 None으로 지정
            data : [[comment, label], [comment, label], ...[comment, label]] 형식으로 input 되어야 함   
        """

        if use_case == "classification":
            if data == None:
                raise ValueError("변환시킬 데이터를 넣어주세요. ex: transform(use_case, data)")
            
            else:
                comment_lists = []
                for comment in data:
                    comment_lists.append(comment[1])

                return comment_lists

        elif use_case == "training":
            data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/labeled_comment (2).csv')
            labeled_list = []

            for comment, label in zip(data['comment_origin'], data['label']):
                data = []
                data.append(comment)
                data.append(str(label))

                labeled_list.append(data)

            return labeled_list


class review_kobert:
    def __init__(self, data):
        """set device, tokenizer, bertmodel and vocab"""
        self.device = torch.device("cuda:0")
        self.tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
        self.tok = self.tokenizer.tokenize 
        self.bertmodel, self.vocab = get_kobert_model('skt/kobert-base-v1', self.tokenizer.vocab_file)

        """파라미터 설정"""
        self.max_len = 64   # BERTDataset hyper-parameter
        self.batch_size = 64   # DataLoader hyper-parameter
        self.learning_rate = 5e-5   # optimizer hyper-parameter
        self.num_epochs = 5   # scheduler pre-hyper-parameter
        self.warmup_ratio = 0.1   # scheduler pre-hyper-parameter
        self.max_grad_norm = 1   
        self.log_interval = 200

        """BERT 데이터 셋으로 변환""" 
        self.data_train = BERTDataset(data, 0, 1, self.tok, self.vocab, self.max_len, True, False)
        self.train_dataloader = torch.utils.data.DataLoader(self.data_train, batch_size=self.batch_size, num_workers=5)
        
        """모델 정의"""
        self.model = BERTClassifier(self.bertmodel,  dr_rate=0.5).to(self.device)

        """optimizer 설정"""
        self.no_decay = ['bias', 'LayerNorm.weight']
        self.optimizer_grouped_parameters = [
            {'params': [p for n, p in self.model.named_parameters() if not any(nd in n for nd in self.no_decay)], 'weight_decay': 0.01},
            {'params': [p for n, p in self.model.named_parameters() if any(nd in n for nd in self.no_decay)], 'weight_decay': 0.0}
        ]
        self.optimizer = AdamW(self.optimizer_grouped_parameters, lr=self.learning_rate)
        self.loss_fn = nn.CrossEntropyLoss()

        """scheduler 설정"""
        self.t_total = len(self.train_dataloader) * self.num_epochs
        self.warmup_step = int(self.t_total * self.warmup_ratio)
        self.schedular = get_cosine_schedule_with_warmup(self.optimizer, num_warmup_steps=self.warmup_step, num_training_steps= self.t_total)


    def train(self):
        for e in range(self.num_epochs):
            train_acc = 0.0
            test_acc = 0.0  
            self.model.train()
            for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm_notebook(self.train_dataloader)):
                self.optimizer.zero_grad()
                token_ids = token_ids.long().to(self.device)
                segment_ids = segment_ids.long().to(self.device)
                valid_length = valid_length
                label = label.long().to(self.device)
                out = self.model(token_ids, valid_length, segment_ids)
                loss = self.loss_fn(out, label)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.max_grad_norm)
                self.optimizer.step()
                self.schedular.step()
                train_acc += self.calc_accuracy(out, label)
                if batch_id % self.log_interval == 0:
                    print("epoch {} batch id {} loss {} train acc {}".format(e+1, batch_id+1, loss.data.cpu().numpy(), train_acc / (batch_id+1)))
            
            print("epoch {} train acc {}".format(e+1, train_acc / (batch_id+1)))


    def predict(self, input_data):
        predict_data = []
        for idx, i in enumerate(input_data):
            i_result = []
            i_result.append(i)

            data = [i, '0']
            dataset_another = [data]

            another_test = BERTDataset(dataset_another, 0, 1, self.tok, self.vocab, self.max_len, True, False)
            input_dataloader = torch.utils.data.DataLoader(another_test, batch_size=self.batch_size, num_workers=5)

            self.model.eval()

            for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(input_dataloader):
                token_ids = token_ids.long().to(self.device)
                segment_ids = segment_ids.long().to(self.device)

                valid_length = valid_length
                label = label.long().to(self.device)
                out = self.model(token_ids, valid_length, segment_ids)

                for index in out:
                    logits = index
                    logits = logits.detach().cpu().numpy()

                    if np.argmax(logits) == 0:
                        i_result.append("피드백")
                    elif np.argmax(logits) == 1:
                        i_result.append("컨텐츠 요구")

            predict_data.append(i_result)

        return predict_data


    def calc_accuracy(self, X, Y): # 정확도 측정을 위한 함수
        self.max_vals, self.max_indices = torch.max(X, 1)
        self.train_acc = (self.max_indices == Y).sum().data.cpu().numpy()/self.max_indices.size()[0]
        
        return self.train_acc

    



# KoBERT 입력 데이터 변환 기능
# 출처: https://velog.io/@seolini43/KOBERT%EB%A1%9C-%EB%8B%A4%EC%A4%91-%EB%B6%84%EB%A5%98-%EB%AA%A8%EB%8D%B8-%EB%A7%8C%EB%93%A4%EA%B8%B0-%ED%8C%8C%EC%9D%B4%EC%8D%ACColab
# KoBERT모델의 입력으로 들어갈 수 있는 형태가 되도록 토큰화, 정수 인코딩, 패딩 등을 해주는 과정
class BERTDataset(review_kobert):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, vocab, max_len, pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, vocab=vocab, pad=pad, pair=pair)
        
        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]
    
    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))
    
    def __len__(self):
        return (len(self.labels))
        

# KoBERT 학습 모델 생성 기능
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
etl = review_etl()

# 훈련시킬 데이터 제작
train_comments = etl.extract(["vWF94oVrK-E"])
train_data = etl.transform("training")

# 분석할 데이터 제작
input_comments = etl.extract(["Mh-ip0PxJK0"]) 
input_data = etl.transform("classification", data=input_comments)

# kobert 클래스 불러옴
kobert = review_kobert(train_data)

# kobert 모델 훈련
kobert.train()

# kobert 모델 예측하고 데이터로 저장
predict_data = kobert.predict(input_data)

# 예측이 되고 나면 예측결과를 기존의 수집 정보 (작성자 닉네임, 좋아요 수 등)에 추가
contents_or_feedback = pd.DataFrame(input_comments, columns=['textDisplay', 'textOriginal', 'authorDisplayName', 'publishedAt', 'likeCount', 'authorProfileImageUrl'])
contents_or_feedback['contents_or_feedback'] = [a[1] for a in predict_data]
contents_or_feedback