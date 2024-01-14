from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from tweety.types import Tweet

from src.sql_alchemy.domain.custom_serializer_mixin import CustomSerializerMixin
from src.sql_alchemy.domain.sql_alchemy import Base


class AccountTwitterPost(Base, CustomSerializerMixin):
    __tablename__ = 'account_twitter_post'
    account_twitter_post_seq: int = Column(Integer, primary_key=True, comment='일렬번호')
    account_seq: int = Column(Integer, ForeignKey('account.account_seq'), nullable=False, comment='계정 일렬번호')
    post_id: int = Column(Integer, nullable=False, comment='트위터 트윗 id')
    like_cnt: int = Column(Integer, nullable=False, default=0, comment='트윗 좋아요 수')
    retweet_cnt: int = Column(Integer, nullable=False, default=0, comment='트윗 리트윗 수')
    bookmark_cnt: int = Column(Integer, nullable=False, default=0, comment='트윗 북마크 수')
    respond_cnt: int = Column(Integer, nullable=False, default=0, comment='트윗 답글 수')
    view_cnt: int = Column(Integer, nullable=False, default=0, comment='트윗 조회수')
    text: str = Column(String(60), nullable=False, default='', comment='포스트 글')
    reg_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='생성 시간')
    update_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='수정 시간')
    scrape_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='정보 획득 시간')

    account = relationship('Account', lazy='noload', back_populates="account_twitter_post")
    youtube_video = relationship('YoutubeVideo', lazy='noload', back_populates="account_twitter_post")

    def __init__(self,
                 account_seq: int = None,
                 post_id: int = None,
                 like_cnt: int = None,
                 retweet_cnt: int = None,
                 bookmark_cnt: int = None,
                 respond_cnt: int = None,
                 view_cnt: int = None,
                 text: str = None,
                 reg_date: datetime = None,
                 update_date: datetime = None,
                 scrape_date: datetime = None,
                 ):
        self.account_seq = account_seq
        self.post_id = post_id
        self.like_cnt = like_cnt
        self.retweet_cnt = retweet_cnt
        self.bookmark_cnt = bookmark_cnt
        self.respond_cnt = respond_cnt
        self.view_cnt = view_cnt
        self.text = text
        self.reg_date = reg_date
        self.update_date = update_date
        self.scrape_date = scrape_date

    def apply_tweet_detail(self, tweet_detail: Tweet):
        self.like_cnt = tweet_detail.likes
        self.retweet_cnt = tweet_detail.retweet_counts
        self.bookmark_cnt = tweet_detail.bookmark_count
        self.respond_cnt = tweet_detail.reply_counts
        if tweet_detail.views != 'Unavailable':
            self.view_cnt = int(tweet_detail.views)
