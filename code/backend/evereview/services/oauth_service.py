import os
import requests
import jwt


CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
API_KEY = os.environ.get("API_KEY")

SCOPE = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube",
]


def authorization(code):
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "postmessage",
        "grant_type": "authorization_code",
    }

    res = requests.post("https://oauth2.googleapis.com/token", data=data)
    oauth_info = res.json()

    if res.status_code == 400:
        return oauth_info

    id_token = oauth_info.get("id_token")
    decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})

    result = {
        "oauth_token": oauth_info.get("access_token"),
        "user_email": decoded_id_token.get("email"),
        "user_name": decoded_id_token.get("name"),
        "user_img": decoded_id_token.get("picture"),
    }

    return result


def fetch_user_channels(oauth_token, admin=False):
    if admin:
        result = []
        static_channels = ["UCIG4gr_wIy5CIlcFciUbIQw"]
        static_channels = fetch_channels(static_channels)
        result += static_channels
        return result

    url = "https://www.googleapis.com/youtube/v3/channels"
    part = ["id", "snippet", "statistics"]
    payload = {
        "key": API_KEY,
        "part": part,
        "mine": True,
    }
    header = {"Authorization": f"Bearer {oauth_token}"}

    res = requests.get(url, params=payload, headers=header)
    channels_info = res.json().get("items")

    if channels_info is None:
        return []

    result = []
    for channel_info in channels_info:
        item = {
            "channel_id": channel_info.get("id"),
            "title": channel_info.get("snippet").get("title"),
            "comment_count": channel_info.get("statistics").get("commentCount"),
            "video_count": channel_info.get("statistics").get("videoCount"),
            "channel_url": "https://www.youtube.com/channel/" + channel_info.get("id"),
            "img_url": channel_info.get("snippet")
            .get("thumbnails")
            .get("default")
            .get("url"),
        }
        result.append(item)

    return result


def fetch_channels(*args):
    url = "https://www.googleapis.com/youtube/v3/channels"
    part = ["id", "snippet", "statistics"]
    payload = {"key": API_KEY, "part": part, "id": args}
    res = requests.get(url, params=payload)
    channels_info = res.json().get("items")

    result = []
    if channels_info is None:
        return result

    for channel_info in channels_info:
        item = {
            "channel_id": channel_info.get("id"),
            "title": channel_info.get("snippet").get("title"),
            "comment_count": channel_info.get("statistics").get("commentCount"),
            "video_count": channel_info.get("statistics").get("videoCount"),
            "channel_url": "https://www.youtube.com/channel/" + channel_info.get("id"),
            "img_url": channel_info.get("snippet")
            .get("thumbnails")
            .get("default")
            .get("url"),
        }
        result.append(item)

    return result


def fetch_videos(channel_id, page=None):
    upload_playlist_id = get_my_uploads_list(channel_id)
    videos_id, page_info, next_page_token, prev_page_token = get_my_uploaded_videos_id(
        upload_playlist_id, page
    )
    videos_details = get_my_uploaded_videos_detail(videos_id)

    return videos_details, page_info, next_page_token, prev_page_token


def search_videos(query, channel_id, page=None):
    (
        searched_videos,
        page_info,
        next_page_token,
        prev_page_token,
    ) = get_my_searched_videos_id(query, channel_id, page)
    videos_details = get_my_uploaded_videos_detail(searched_videos)

    return videos_details, page_info, next_page_token, prev_page_token


def get_my_searched_videos_id(query, channel_id, page=None):
    url = "https://www.googleapis.com/youtube/v3/search"
    part = ["id"]
    payload = {
        "key": API_KEY,
        "part": part,
        "q": query,
        "channelId": channel_id,
        "maxResults": 50,
        "pageToken": page,
    }
    res = requests.get(url, params=payload)
    page_info = res.json().get("pageInfo")
    next_page_token = res.json().get("nextPageToken")
    prev_page_token = res.json().get("prevPageToken")
    items = res.json().get("items")

    result = []
    if items:
        result = list(map(lambda item: item.get("id").get("videoId"), items))

    return result, page_info, next_page_token, prev_page_token


def get_my_uploads_list(channel_id):
    url = "https://www.googleapis.com/youtube/v3/channels"
    part = ["contentDetails"]
    payload = {"key": API_KEY, "part": part, "id": channel_id}
    res = requests.get(url, params=payload)
    playlist_id = (
        res.json()
        .get("items")[0]
        .get("contentDetails")
        .get("relatedPlaylists")
        .get("uploads")
    )

    return playlist_id


def get_my_uploaded_videos_id(playlist_id, page=None):
    url = "https://www.googleapis.com/youtube/v3/playlistItems"
    part = ["contentDetails"]
    payload = {
        "key": API_KEY,
        "part": part,
        "playlistId": playlist_id,
        "maxResults": 50,
        "pageToken": page,
    }
    res = requests.get(url, params=payload)
    page_info = res.json().get("pageInfo")
    next_page_token = res.json().get("nextPageToken")
    prev_page_token = res.json().get("prevPageToken")
    playlist_items = res.json().get("items")

    result = []

    if playlist_items is None:
        return result, page_info, next_page_token, prev_page_token

    for playlist_item in playlist_items:
        video_id = playlist_item.get("contentDetails").get("videoId")
        result.append(video_id)

    return result, page_info, next_page_token, prev_page_token


def get_my_uploaded_videos_detail(*args):
    url = "https://www.googleapis.com/youtube/v3/videos"
    part = ["snippet", "statistics"]
    payload = {
        "key": API_KEY,
        "part": part,
        "id": args,
    }
    res = requests.get(url, params=payload)
    video_items = res.json().get("items")

    result = []
    if video_items is None:
        return result

    for video_item in video_items:
        item = {
            "id": video_item.get("id"),
            "title": video_item.get("snippet").get("title"),
            "channel_id": video_item.get("snippet").get("channelId"),
            "published_at": video_item.get("snippet").get("publishedAt"),
            "thumbnail_url": video_item.get("snippet")
            .get("thumbnails")
            .get("medium")
            .get("url"),
            "category_id": video_item.get("snippet").get("categoryId"),
            "view_count": video_item.get("statistics").get("viewCount"),
            "like_count": video_item.get("statistics").get("likeCount"),
            "comment_count": video_item.get("statistics").get("commentCount"),
        }
        result.append(item)

    return result
