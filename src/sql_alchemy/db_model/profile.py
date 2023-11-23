import os
from datetime import datetime
from pathlib import Path
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from src.sql_alchemy.domain.sql_alchemy import Base
from src.sql_alchemy.domain.custom_serializer_mixin import CustomSerializerMixin


class Profile(Base, CustomSerializerMixin):
    __tablename__ = 'profile'
    profile_seq: int = Column(Integer, primary_key=True, comment='프로필 일렬번호')
    profile_name: str = Column(String(100), nullable=False, comment='프로필명')
    user_agent: str = Column(String(300), nullable=False, comment='프로필 user-agent')
    s3_object: str = Column(String(100), nullable=False, comment='프로필 s3 오브젝트')
    reg_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='생성 시간')
    update_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='수정 시간')

    account = relationship('Account', lazy='noload', back_populates="profile")

    def __init__(self,
                 profile_name: str,
                 user_agent: str,
                 s3_object: str,
                 profile_seq: int = None,
                 reg_date: datetime = None,
                 update_date: datetime = None,
                 ):
        self.profile_seq = profile_seq
        self.profile_name = profile_name
        self.user_agent = user_agent
        self.s3_object = s3_object
        self.reg_date = reg_date
        self.update_date = update_date

        if reg_date is None:
            self.reg_date = datetime.now()
        if update_date is None:
            self.update_date = datetime.now()

    def get_profile_dir(self) -> Path:
        return Path(os.path.join(os.getcwd(), Path(f'external-files/profiles/{self.profile_name}')))

    def get_profile_zip_dir(self) -> Path:
        return self.get_profile_dir().with_suffix('.zip')

    def get_storage_dir(self) -> Path:
        return Path(os.path.join(os.getcwd(), Path(f'external-files/profiles/{self.profile_name}.pkl')))
