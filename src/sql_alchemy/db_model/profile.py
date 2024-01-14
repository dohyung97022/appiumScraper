from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.sql_alchemy.domain.sql_alchemy import Base
from src.sql_alchemy.domain.custom_serializer_mixin import CustomSerializerMixin


class Profile(Base, CustomSerializerMixin):
    __tablename__ = 'profile'
    profile_seq: int = Column(Integer, primary_key=True, comment='프로필 일렬번호')
    profile_name: str = Column(String(100), nullable=True, comment='프로필명')
    user_agent: str = Column(String(300), nullable=True, comment='프로필 user-agent')
    cookie: str = Column(String(1000), nullable=True, comment='프로필 cookie')
    s3_object: str = Column(String(100), nullable=True, comment='프로필 s3 오브젝트')
    reg_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='생성 시간')
    update_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='수정 시간')

    account = relationship('Account', lazy='noload', back_populates="profile")

    def __init__(self,
                 profile_seq: int = None,
                 profile_name: str = None,
                 user_agent: str = None,
                 cookie: str = None,
                 s3_object: str = None,
                 reg_date: datetime = None,
                 update_date: datetime = None,
                 ):
        self.profile_seq = profile_seq
        self.profile_name = profile_name
        self.user_agent = user_agent
        self.cookie = cookie
        self.s3_object = s3_object
        self.reg_date = reg_date
        self.update_date = update_date

        if reg_date is None:
            self.reg_date = datetime.now()
        if update_date is None:
            self.update_date = datetime.now()
