import os
import numpy as np
import pandas as pd

from googleapiclient.discovery import build


class review_etl:
    def extract(self, video_id=None, channel_id=None, day_start=None, day_end=None):
        api_key = os.environ.get("API_KEY")
        api_obj = build("youtube", "v3", developerKey=api_key)
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
                response = (
                    api_obj.commentThreads()
                    .list(part="snippet,replies", videoId=video, maxResults=100)
                    .execute()
                )  # execute로 html코드 풀어줌

                # while문 이용하여 각 영상에 대한 댓글을 페이지네이션 하여 모두 불러온다.
                while response:
                    for item in response["items"]:
                        comment_id = item["id"]
                        comment = item["snippet"]["topLevelComment"]["snippet"]

                        # 리스트 요소 설명 상기 함수 주석 참고
                        comments.append(
                            [
                                comment_id,
                                comment["videoId"],
                                comment["authorDisplayName"],
                                comment["authorProfileImageUrl"],
                                comment["textDisplay"],
                                comment["textOriginal"],
                                comment["likeCount"],
                                comment["publishedAt"],
                            ]
                        )

                    # 댓글의 끝 페이지 요청에서 다음페이지로 가는 토큰이 있을 경우 그 토큰>을 다음 api 요청으로 함
                    if "nextPageToken" in response:
                        response = (
                            api_obj.commentThreads()
                            .list(
                                part="snippet,replies",
                                videoId=video,
                                pageToken=response["nextPageToken"],
                                maxResults=100,
                            )
                            .execute()
                        )
                    else:
                        break

            # 선택된 기간에 맞는 데이터만 포함시키도록 전처리
            # str(2021-09-22T14:39:22Z) --> int(20210922)
            result_df = pd.DataFrame(
                comments,
                columns=[
                    "id",
                    "video_id",
                    "author",
                    "author_img",
                    "text_display",
                    "text_original",
                    "like_count",
                    "published_at",
                ],
            )
            result_df["published_at"] = result_df["published_at"].apply(
                lambda x: int(x[0:4] + x[5:7] + x[8:10])
            )

            comments = result_df

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
            if not channel_id:
                raise ValueError("채널 id를 입력해주세요 channel_id = ?")
            if not day_start:
                raise ValueError("댓글 시작 기간을 입력해주세요. day_start = ?")
            if not day_end:
                raise ValueError("댓글 끝 기간을 입력해주세요. day_end = ?")

            # channel 에 있는 정보 불러옴
            response_channel = (
                api_obj.channels().list(part="contentDetails", id=channel_id).execute()
            )

            # 받아온 channel의 영상 목록 id 받아옴
            playlist = response_channel["items"][0]["contentDetails"][
                "relatedPlaylists"
            ]["uploads"]

            # 플레이 리스트에 있는 영상을 받아옴 : maxResult가 50개인데, 추후에 next page Token을 활용하여 모든 영상을 불러오는 코드를 짜려고 합니다.
            response_playlists = (
                api_obj.playlistItems()
                .list(part="contentDetails", playlistId=playlist, maxResults=50)
                .execute()
            )

            all_video_id = []
            for res in response_playlists["items"]:
                all_video_id.append(res["contentDetails"]["videoId"])

            # 이 반복 코드는 영상별 수집 코드와 동일합니다.
            for video_id in all_video_id:
                response = (
                    api_obj.commentThreads()
                    .list(part="snippet,replies", videoId=video_id, maxResults=100)
                    .execute()
                )

                while response:
                    for item in response["items"]:
                        comment_id = item["id"]
                        comment = item["snippet"]["topLevelComment"]["snippet"]

                        comments.append(
                            [
                                comment_id,
                                comment["videoId"],
                                comment["authorDisplayName"],
                                comment["authorProfileImageUrl"],
                                comment["textDisplay"],
                                comment["textOriginal"],
                                comment["likeCount"],
                                comment["publishedAt"],
                            ]
                        )

                    if "nextPageToken" in response:
                        response = (
                            api_obj.commentThreads()
                            .list(
                                part="snippet,replies",
                                videoId=video_id,
                                pageToken=response["nextPageToken"],
                                maxResults=100,
                            )
                            .execute()
                        )
                    else:
                        break

            # 선택된 기간에 맞는 데이터만 포함시키도록 전처리
            # str(2021-09-22T14:39:22Z) --> int(20210922)
            result_df = pd.DataFrame(
                comments,
                columns=[
                    "id",
                    "video_id",
                    "author",
                    "author_img",
                    "text_display",
                    "text_original",
                    "like_count",
                    "published_at",
                ],
            )
            result_df["published_at"] = result_df["published_at"].apply(
                lambda x: int(x[0:4] + x[5:7] + x[8:10])
            )

            # 쿼리문
            result_df = (
                result_df[
                    (result_df["published_at"] >= day_start)
                    & (result_df["published_at"] <= day_end)
                ]
                .reset_index()
                .iloc[:, 1:]
            )
            comments = result_df

            return comments

        else:
            raise ValueError("올바른 매개변수를 입력해주세요")

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
                comment_lists.append(comment[3])

            return comment_lists
