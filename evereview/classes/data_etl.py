import numpy as np
import pandas as pd

from googleapiclient.discovery import build

class review_etl:
    def extract(self, video_id=None, channel_id=None, day_start=None, day_end=None):
        api_key = "AIzaSyCrzeLdyyZ8k6oBUXm2AeyX20GYV83novM"
        api_obj = build('youtube', 'v3', developerKey=api_key)
        comments = list()

        # 영상별 수집
        if video_id:
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
                'authorDisplayName' : 댓글 작성자 닉네임
                'authorProfileImageUrl' : 댓글 작성자의 썸네일 Url
                'textDisplay' : 댓글의 html 코드, 텍스트
                'textOriginal' : 댓글의 텍스트
                'likeCount' : 댓글의 좋아요 수
                'publishedAt' : 댓글 최초 작성 일자
            """
            for video in video_id:
                response = api_obj.commentThreads().list(part='snippet,replies', videoId=video, maxResults=100).execute() # execute로 html코드 풀어줌

                # while문 이용하여 각 영상에 대한 댓글을 페이지네이션 하여 모두 불러온다.
                while response:

                    # 코드 수정 부분 : 고정 메시지는 추가 안하도록 함 (최신순에 상관없이 제일 먼저 수집되기 때문)
                    for item in response['items'][1:]:
                        comment = item['snippet']['topLevelComment']['snippet']

                        # 리스트 요소 설명 상기 함수 주석 참고
                        comments.append([comment['authorDisplayName'], comment['authorProfileImageUrl'], comment['textDisplay'], 
                                         comment['textOriginal'], comment['likeCount'], comment['publishedAt']])

                    # 댓글의 끝 페이지 요청에서 다음페이지로 가는 토큰이 있을 경우 그 토큰>을 다음 api 요청으로 함
                    if 'nextPageToken' in response:
                        response = api_obj.commentThreads().list(part='snippet,replies',
                                                                    videoId=video,
                                                                    pageToken=response['nextPageToken'],
                                                                    maxResults=100).execute()
                    else:
                        break

            result_df = pd.DataFrame(comments, columns=['authorDisplayName', 'authorProfileImageUrl', 'textDisplay', 'textOriginal', 'likeCount', 'publishedAt'])
            
            # 코드 수정 부분 : publishedAt 형식 맞춤
            result_df['publishedAt'] = result_df['publishedAt'].apply(lambda x: (x[0:4] + "-" + x[5:7] + "-" + x[8:10]))
            comments = result_df.values.tolist()

            return comments
        

        # 댓글 기간별 수집
        elif not video_id:
            """
            <Parmeter>
                - channel_id
                설명 : 유튜버 채널 아이디
                형식 : 문자열 ex ) "UChxh4uh0d3OOeRhm-5pv6bA"

                - day_start
                설명 : 댓글 작성 시작 기간
                형식 : int 형 ex ) 20200203

                - day_end
                설명 : 댓글 작성 끝 기간
                형식 : int 형 ex ) 20210210

            <return>
                - comments
                설명 : 해당 영상에 달린 모든 최신 댓글 리스트 출력
                형식 : 중첩 리스트 (ex : [댓글 리스트1, 댓글 리스트2, 댓글 리스트3])

                <댓글 리스트 요소 설명>
                'authorDisplayName' : 댓글 작성자 닉네임
                'authorProfileImageUrl' : 댓글 작성자의 썸네일 Url
                'textDisplay' : 댓글의 html 코드, 텍스트
                'textOriginal' : 댓글의 텍스트
                'likeCount' : 댓글의 좋아요 수
                'publishedAt' : 댓글 최초 작성 일자
            """
            if not channel_id : raise ValueError("채널 id를 입력해주세요 channel_id = ?")
            if not day_start : raise ValueError("댓글 시작 기간을 입력해주세요. day_start = ?")
            if not day_end : raise ValueError("댓글 끝 기간을 입력해주세요. day_end = ?")

            # channel 에 있는 정보 불러옴
            response_channel = api_obj.channels().list(part="contentDetails", id=channel_id).execute()
            
            # 받아온 channel의 영상 목록 id 받아옴
            playlist = response_channel['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            response_playlists = api_obj.playlistItems().list(part="contentDetails", playlistId=playlist, maxResults=50).execute()

            # 코드 수정 부분 : 모든 플레이리스트가 들어갈 변수 [플레이리스트1, 플레이리스트2, ...]
            playlist_list = [response_playlists]

            # 코드 수정 부분 : playlists 끝까지 받아오도록 함
            while response_playlists:
                if 'nextPageToken' in response_playlists:
                    response_playlists = api_obj.playlistItems().list(part="contentDetails", playlistId=playlist,
                                                                      maxResults=50, pageToken=response_playlists['nextPageToken']).execute()
                    playlist_list.append(response_playlists)

                else: break

            # 코드 수정 부분 : 모든 video_id가 들어갈 변수 ['video_id_1', ''video_id_2', ...]
            all_video_id = []

            for playlist in playlist_list:
                for res in playlist['items']:
                    all_video_id.append(res['contentDetails']['videoId'])

            # 코드 수정 부분 : 주석 처리
            # break_count = 0

            # 이 반복 코드는 영상별 수집 코드와 동일합니다.
            for video_id in all_video_id:

                # 코드 수정 부분 : 주석 처리
                # if break_count == 49:
                #     break
                # break_count+=1

                print(f"{video_id} 댓글 수집중...")
                response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute() 

                # 코드 수정 부분 : while 문 전체 코드 수정, 댓글 수집 요청 최소화
                while response:

                    # 고정 메시지는 추가 안하도록 슬라이싱함 (최신순에 상관없이 제일 먼저 수집되기 때문)
                    for item in response['items'][1:]:
                        comment = item['snippet']['topLevelComment']['snippet']
                        
                        # 날짜 계산 위한 변수 : str(2021-09-22T14:39:22Z) --> int(20210922)
                        comment_time_int = int(comment['publishedAt'][0:4] + comment['publishedAt'][5:7] + comment['publishedAt'][8:10]) 
                        
                        # 작성된 댓글 날짜가 day_end보다 더 이전이면 댓글 수집  
                        if comment_time_int <= day_end:
                             # 작성된 댓글 날짜가 day_start보다도 더 이전이면 break
                            if comment_time_int < day_start:
                                break

                            # 모든 조건 걸러지면 수집, 날짜 형식 통일 위해 publishedAt 부분 슬라이싱 함    
                            comments.append([comment['authorDisplayName'], comment['authorProfileImageUrl'], comment['textDisplay'], 
                                            comment['textOriginal'], comment['likeCount'], comment['publishedAt'][0:10]])                           


                    if 'nextPageToken' in response:
                        response = api_obj.commentThreads().list(part='snippet,replies',
                                                                    videoId=video_id,
                                                                    pageToken=response['nextPageToken'],
                                                                    maxResults=100).execute()
                    else:
                        break

            return comments


        else: raise ValueError("올바른 매개변수를 입력해주세요")


    def transform(self, data=None, test=0):
        """
        <parameter>
        - data : 변환을 수행할 데이터
            default : 파라미터 미 지정 시 None으로 지정
            data : [[comment, col1, col2, ...], [comment, col1, col2, ...]] 형식으로 input 되어야 함   
        """
        if data == None:
            raise ValueError("변환시킬 데이터를 넣어주세요. ex: transform(use_case, data)")

        else:
            comment_lists = []
            for comment in data:
                if test == 1:
                    comment_lists.append(comment[0])
                else : comment_lists.append(comment[3])

            return comment_lists