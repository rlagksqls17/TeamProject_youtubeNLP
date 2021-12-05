import torch
from torch import nn

import numpy as np
import pandas as pd
import gluonnlp as nlp

from googleapiclient.discovery import build  
from kobert.pytorch_kobert import get_kobert_model
from kobert_tokenizer import KoBERTTokenizer



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
        feedback_classifier = torch.load('/datadrive/TeamProject_youtubeNLP/evereview/model/feedback_classifier')
        goodbad_classifier = torch.load('/datadrive/TeamProject_youtubeNLP/evereview/model/goodbad_classifier_movie2')

        for idx, i in enumerate(input_data):
            count += 1
            print(i)
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
                                    print("bad_feedback")
                                    i_result.append("bad_feedback")
                                elif np.argmax(goodbad_logits) == 1:
                                    print("good_feedback")
                                    i_result.append("good_feedback")

                    elif np.argmax(feedback_logits) == 1:
                        print("contents")
                        i_result.append("contents")

            predict_data.append(i_result)

        return predict_data
