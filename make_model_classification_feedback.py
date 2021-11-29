import torch
from torch import nn
import torch.nn.functional as F

import pandas as pd
import numpy as np

import re
import gluonnlp as nlp
from soynlp.normalizer import *

from kobert_tokenizer import KoBERTTokenizer
from kobert.pytorch_kobert import get_kobert_model
from sklearn.model_selection import train_test_split

from transformers import AdamW  
from transformers.optimization import get_cosine_schedule_with_warmup

from tqdm import tqdm_notebook 



# KoBERT 입력 데이터로 만들기
# 출처: https://velog.io/@seolini43/KOBERT%EB%A1%9C-%EB%8B%A4%EC%A4%91-%EB%B6%84%EB%A5%98-%EB%AA%A8%EB%8D%B8-%EB%A7%8C%EB%93%A4%EA%B8%B0-%ED%8C%8C%EC%9D%B4%EC%8D%ACColab
# KoBERT모델의 입력으로 들어갈 수 있는 형태가 되도록 토큰화, 정수 인코딩, 패딩 등을 해주는 과정
class BERTDataset(Dataset):
    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, vocab, max_len, pad, pair):
        transform = nlp.data.BERTSentenceTransform(
            bert_tokenizer, max_seq_length=max_len, vocab=vocab, pad=pad, pair=pair)
        
        self.sentences = [transform([i[sent_idx]]) for i in dataset]
        self.labels = [np.int32(i[label_idx]) for i in dataset]
    
    def __getitem__(self, i):
        return (self.sentences[i] + (self.labels[i], ))
    
    def __len__(self):
        return (len(self.labels))


# KoBERT 학습 모델 만들기
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


#정확도 측정을 위한 함수 정의
def calc_accuracy(X,Y):
    max_vals, max_indices = torch.max(X, 1)
    train_acc = (max_indices == Y).sum().data.cpu().numpy()/max_indices.size()[0]
    return train_acc


# train-test dataset 전저리 함수
def preprocess_train_dataset(raw_dataframe):
    # 댓글-라벨 페어 df를 중첩 list로 변환
    raw_df_list = []

    for comment, label in zip(raw_df['comment_origin'], raw_df['label']):
        data = []
        data.append(comment)
        data.append(str(label))

        raw_df_list.append(data)
    
    # 기본 전처리
    result = []
    for line in raw_df_list:
        comment = line[0]
        label = line[1]
        
        # 한글만 추출 (외국어, 특수문자, 이모티콘, 문장부호, 숫자 제거)
        only_korean = only_hangle(comment)

        # 한글 자모 제거 (ex. ㅋㅋ, ㅠㅠ 등)
        pattern = re.compile("[ㄱ-ㅎ]")
        without_letters = pattern.sub("", only_korean)

        result.append([without_letters, label])
    
    # 전처리 결과 빈 문자열 된 댓글들은 삭제 후 processed 리스트를 df로
    processed = []
    for line in result:
        comment = line[0]
        label = line[1]
        if comment == '':
            pass
        else:
            processed.append(line)

    return processed




"""set device, tokenizer, bertmodel and vocab"""
device = torch.device("cuda:0")
tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
tok = tokenizer.tokenize
bertmodel, vocab = get_kobert_model('skt/kobert-base-v1', tokenizer.vocab_file)

"""파라미터 설정"""
max_len = 64   # BERTDataset hyper-parameter
batch_size = 64   # DataLoader hyper-parameter
learning_rate = 5e-5   # optimizer hyper-parameter
num_epochs = 5   # scheduler pre-hyper-parameter
warmup_ratio = 0.1   # scheduler pre-hyper-parameter
max_grad_norm = 1   
log_interval = 200

"""데이터 로드"""
raw_df = pd.read_csv('경로 수정 / fr_classification_df.csv')

"""데이터 전처리"""
processed = preprocess_train_dataset(raw_df)

"""데이터 분할"""
dataset_train, dataset_test = train_test_split(processed, test_size=0.3, random_state=0)

"""BERT 데이터 셋으로 변환""" 
data_train = BERTDataset(dataset_train, 0, 1, tok, vocab, max_len, True, False)
train_dataloader = torch.utils.data.DataLoader(data_train, batch_size=batch_size, num_workers=2)

"""모델 정의"""
model = BERTClassifier(bertmodel,  dr_rate=0.5).to(device)

"""optimizer 설정"""
no_decay = ['bias', 'LayerNorm.weight']
optimizer_grouped_parameters = [
    {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
    {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
]
optimizer = AdamW(optimizer_grouped_parameters, lr=learning_rate)
loss_fn = nn.CrossEntropyLoss()


"""scheduler 설정"""
t_total = len(train_dataloader) * num_epochs
warmup_step = int(t_total * warmup_ratio)
scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=warmup_step, num_training_steps=t_total)


# KoBERT 모델 학습시키기
# 학습 데이터셋과 학습 모델 준비가 끝났으니 이제 학습을 시켜보자
for e in range(num_epochs):
    train_acc = 0.0
    test_acc = 0.0
    model.train()
    for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm_notebook(train_dataloader)):
        optimizer.zero_grad()
        token_ids = token_ids.long().to(device)
        segment_ids = segment_ids.long().to(device)
        valid_length= valid_length
        label = label.long().to(device)
        out = model(token_ids, valid_length, segment_ids)
        loss = loss_fn(out, label)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
        optimizer.step()
        scheduler.step()  # Update learning rate schedule
        train_acc += calc_accuracy(out, label)
        if batch_id % log_interval == 0:
            print("epoch {} batch id {} loss {} train acc {}".format(e+1, batch_id+1, loss.data.cpu().numpy(), train_acc / (batch_id+1)))
    
    print("epoch {} train acc {}".format(e+1, train_acc / (batch_id+1)))

# saving the model
torch.save(model, '경로 수정 / first_classifier')