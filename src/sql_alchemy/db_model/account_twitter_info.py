from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from tweety.types import User

from src.sql_alchemy.domain.custom_serializer_mixin import CustomSerializerMixin
from src.sql_alchemy.domain.sql_alchemy import Base


class AccountTwitterInfo(Base, CustomSerializerMixin):
    __tablename__ = 'account_twitter_info'
    account_twitter_info_seq: int = Column(Integer, primary_key=True, comment='트위터 계정 정보 테이블')
    account_seq: int = Column(Integer, ForeignKey('account.account_seq'), nullable=False, comment='계정 일렬번호')
    profile_interstitial_type: str = Column(String, comment='트위터 계정 분류')
    is_default_profile_image: bool = Column(Boolean, comment='트위터 프로필 이미지 미설정 여부')
    followers_count: int = Column(Integer, comment='트위터 팔로워 수')
    friends_count: int = Column(Integer, comment='트위터 팔로잉 수')
    reg_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='생성 시간')
    update_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='수정 시간')
    scrape_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='정보 획득 시간')

    account = relationship('Account', lazy='noload', back_populates="account_twitter_info")

    def __init__(self,
                 account_twitter_info_seq: int = None,
                 account_seq: int = None,
                 profile_interstitial_type: str = None,
                 is_default_profile_image: bool = None,
                 followers_count: int = None,
                 friends_count: int = None,
                 reg_date: datetime = None,
                 update_date: datetime = None,
                 scrape_date: datetime = None,
                 user: User = None,
                 ):
        self.account_twitter_info_seq = account_twitter_info_seq
        self.account_seq = account_seq
        self.profile_interstitial_type = profile_interstitial_type
        self.is_default_profile_image = is_default_profile_image
        self.followers_count = followers_count
        self.friends_count = friends_count
        if reg_date is None:
            self.reg_date = datetime.now()
        if update_date is None:
            self.update_date = datetime.now()
        if scrape_date is None:
            self.scrape_date = datetime.now()
        if user is not None:
            self.apply_user(user)

    def apply_user(self, user: User):
        self.followers_count = user.followers_count
        self.friends_count = user.friends_count
        self.profile_interstitial_type = user.profile_interstitial_type
        self.is_default_profile_image = user.get('original_user').get('default_profile_image')
