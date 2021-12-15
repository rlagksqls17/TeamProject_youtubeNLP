import pandas as pd
import numpy as np  

import re
from soynlp.normalizer import *

from pororo import Pororo

from sklearn.cluster import DBSCAN



"""
기본 전처리 수행 함수
- input: 댓글 내용이 담겨있는 'textOriginal' 컬럼과 피드백인지 컨텐츠 요구인지에 대한 예측결과가 담겨있는 'predict' 컬럼을 포함한 dataframe
- output : 파라미터로 받은 df에 전처리 된 댓글이 담긴 새로운 컬럼이 추가되어 반환됨
"""
def preprocess_comments(raw_dataframe):

    # 전처리 된 댓글을 담을 리스트 생성
    preprocessed_list = list()

    for comment in raw_dataframe['textOriginal']:

        # 한글만 추출
        only_korean = only_hangle_number(comment)
        
        # 한글 자모 제거 (ex. ㅋㅋ, ㅠㅠ 등)
        pattern = re.compile("[ㄱ-ㅎ]")
        without_letters = pattern.sub("", only_korean)

        # 전처리된 댓글 without_letters 한 건을 차례로 'preprocessed_list'에 추가
        preprocessed_list.append(without_letters)

        
    # 파라미터로 전달받은 df의 모든 댓글 전처리가 완료되면
    # 전처리된 댓글이 담긴 리스트를 시리즈로 변환한 것을 기존 df에 컬럼으로 추가
    preprocessed = pd.Series(preprocessed_list, name="preprocessed")
    result = pd.concat([raw_dataframe, preprocessed], axis=1)

    return result

"""
pororo 이용해서 임베딩 해주는 함수
- input: preprocess_comments 함수를 통해 얻은 df ('preprocessed' 컬럼 포함)
- output : 입력받은 df에서 preprocessed 컬럼의 내용을 임베딩하고 각 로우에 맞는 데이터를 옆의 새 컬럼에 추가한 df ('embedded' 컬럼 추가)
"""
def embedding(preprocessed_data):

    # pororo 모델 불러오기
    model = Pororo(task="sentence_embedding", lang="ko")
    
    # 임베딩 결과를 차례로 담을 리스트 생성
    embeddings_list = list()

    # df에서 전처리 된 댓글이 들어있는 preprocessed 컬럼을 돌면서
    for sentence in preprocessed_data['preprocessed']:
        # 전처리 된 댓글이 빈 문자열이 아닌 경우:
        if sentence != "":
            # 댓글을 하나하나 임베딩하고 그 결과를 차례로 embeddings_list에 추가
            embeddings_list.append(model(sentence))
        else:
            embeddings_list.append(None)
    
    # 모든 댓글 임베딩을 완료하면
    # embeddings 리스트를 시리즈로 바꾸고 입력 df에 새 컬럼으로 추가  
    preprocessed_data['embedded'] = embeddings_list

    return preprocessed_data


"""
embedding 함수를 거친 df를 파라미터로 받아서 dbscan으로 군집화 진행  
여기서 dbscan 파라미터 값 계속 변화시키면서 그 결과에 대해 시각화  
"""
def proceed_dbscan(data, eps=0.1, min_samples=5):

    # 임베딩 정보만 나타낼 df 생성
    # 행의 갯수 = 댓글 수, 열의 갯수 = 임베딩된 정보 차원인 사이즈의 df를 np.nan값으로 채워 생성한다.  
    embedding_df = pd.DataFrame(np.nan, index=[i for i in range(len(data))], 
                                        columns=[i for i in range(len(data.embedded.iloc[0]))])
    
    # 'embedded' 컬럼의 데이터만 가져와 각 행은 댓글 하나 정보를 나타내고, 컬럼은 차원을 나타내는 embedded_tmp 생성  
    # 0부터 댓글 수까지 위에서 생성한 데이터 프레임의 행을 돌면서
    for i in range(len(data['embedded'])):
        # 임베딩 정보를 칸에 맞게 집어 넣어 값을 교체해준다. 
        embedding_df.iloc[i] = data['embedded'].iloc[i]

    # embedded_df를 DBSCAN 함수의 fit 메서드에 파라미터로 줘서 결과를 얻음
    dbscanned = DBSCAN(eps=eps, min_samples=min_samples).fit(embedding_df.values)
    # 파라미터로 입력받은 df에 군집화 결과를 담은 새 컬럼을 추가하고 리턴한다.
    data['dbscanned'] = dbscanned.labels_

    result = data

    return result
    


