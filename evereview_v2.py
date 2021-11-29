from googleapiclient.discovery import build  


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




# 객체 생성
etl = review_etl()

# 분석할 데이터 제작
input_comments = etl.extract(["Mh-ip0PxJK0"]) 
input_data = etl.transform(data=input_comments)



# kobert 모델 예측하고 데이터로 저장
predict_data = kobert.predict(input_data)

# 예측이 되고 나면 예측결과를 기존의 수집 정보 (작성자 닉네임, 좋아요 수 등)에 추가
contents_or_feedback = pd.DataFrame(input_comments, columns=['textDisplay', 'textOriginal', 'authorDisplayName', 'publishedAt', 'likeCount', 'authorProfileImageUrl'])
contents_or_feedback['contents_or_feedback'] = [a[1] for a in predict_data]
contents_or_feedback