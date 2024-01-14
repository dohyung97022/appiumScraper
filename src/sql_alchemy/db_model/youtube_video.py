from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.sql_alchemy.domain.custom_serializer_mixin import CustomSerializerMixin
from src.sql_alchemy.domain.sql_alchemy import Base
from src.youtube.domain.video import Video


class YoutubeVideo(Base, CustomSerializerMixin):
    __tablename__ = 'youtube_video'
    youtube_video_seq: int = Column(Integer, primary_key=True, comment='일렬번호')
    account_twitter_post_seq: int = Column(Integer, ForeignKey('account_twitter_post.account_twitter_post_seq'),
                                           comment='트위터 포스트 일럴번호')
    video_id: str = Column(String(30), unique=True, nullable=False, comment='유튜브 영상 id')
    title: str = Column(String(120), nullable=False, comment='유튜브 영상 제목')
    keyword: str = Column(String(60), nullable=False, comment='검색어')
    chip_key: str = Column(String(30), comment='Shorts 와 같은 옵션')
    reg_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='생성 시간')
    update_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='수정 시간')

    account_twitter_post = relationship('AccountTwitterPost', lazy='joined', back_populates="youtube_video")

    def __init__(self,
                 video_id: str = None,
                 keyword: str = None,
                 chip_key: str = None,
                 reg_date: datetime = None,
                 update_date: datetime = None,
                 video: Video = None,
                 ):
        self.video_id = video_id
        self.keyword = keyword
        self.chip_key = chip_key
        self.reg_date = reg_date
        self.update_date = update_date
        if video is not None:
            self.apply_video(video)
        if reg_date is None:
            self.reg_date = datetime.now()
        if update_date is None:
            self.update_date = datetime.now()

    def apply_video(self, video: Video):
        self.video_id = video.video_id
        self.title = video.title

    @staticmethod
    def parse_videos(videos: list[Video], keyword: str = None, chip_key: str = None) -> list:
        youtube_videos = []
        for video in videos:
            youtube_videos.append(YoutubeVideo(video=video, keyword=keyword, chip_key=chip_key))
        return youtube_videos
