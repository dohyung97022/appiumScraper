import json
import requests as requests

from src.sql_alchemy.db_model.youtube_video import YoutubeVideo
from src.sql_alchemy.db_service.youtube_video.service import youtube_video_service
from src.utils.log.log_utils import CustomLogger
from src.youtube.domain.chip import Chip
from src.youtube.domain.continuation import Continuation
from src.youtube.domain.video import Video

client = {"hl": "en", "gl": "US", "clientName": "WEB", "clientVersion": "2.20240102.07.00"}


def search(keyword: str):
    result = requests.session().post("https://www.youtube.com/youtubei/v1/search",
                                     params={},
                                     json={"context": {"client": client}, "query": keyword},
                                     headers={})
    return json.loads(result.content)


def search_continuation(token: str):
    s = requests.session()
    result = s.post("https://www.youtube.com/youtubei/v1/search",
                    params={},
                    json={"context": {"client": client}, "continuation": token},
                    headers={"authorization": "SAPISIDHASH 1704335617_e72d02a68243c61b04537b1165b33b55c3f77224"},
                    cookies={"SID": "eQjmpTcUzMuH5U56JNd8kP1GZQzyEJcOGNH_EQyn4pFSO783JY6YqRhhSd6os_yNx5NaBa."})
    return json.loads(result.content)


def loop_scrape_videos(keyword: str, chip_key: str, cnt: int):
    content = search(keyword)
    chip = Chip(content)
    token = chip.name_to_token[chip_key]
    videos = []

    for i in range(cnt):
        content = search_continuation(token)
        videos.extend(Video.parse_videos(content))
        continuation = Continuation(content)
        token = continuation.token

    youtube_videos = YoutubeVideo.parse_videos(videos, keyword, chip_key)
    for youtube_video in youtube_videos:
        youtube_video_service.insert_youtube_video(youtube_video)
    CustomLogger().info("youtube video scrape success.")
