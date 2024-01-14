from src.utils.object.object_utils import find_key_by_name, find_keys_by_name


class Video:
    video_id: str
    title: str
    thumbnail_url: str
    views: str
    reg_date: str

    def __init__(self, content: dict):
        self.video_id = find_key_by_name(content, 'videoId')
        title = find_key_by_name(content, 'title')
        self.title = find_key_by_name(title, 'text')
        thumbnails = find_keys_by_name(content, "thumbnails")
        self.thumbnail_url = find_key_by_name(thumbnails, 'url')
        view_count_text = find_key_by_name(content, 'viewCountText')
        self.views = find_key_by_name(view_count_text, 'simpleText')
        published_time_text = find_key_by_name(content, 'publishedTimeText')
        self.reg_date = find_key_by_name(published_time_text, 'simpleText')

    @staticmethod
    def parse_videos(content: dict) -> list:
        result = []
        video_renders = find_keys_by_name(content, "videoRenderer")
        for video_render in video_renders:
            result.append(Video(video_render))
        return result
