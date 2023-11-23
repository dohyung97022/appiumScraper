from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.sql_alchemy.db_model.account_tag_association import AccountTagAssociation
from src.sql_alchemy.db_model.account_twitter_info import AccountTwitterInfo
from src.sql_alchemy.db_model.profile import Profile
from src.sql_alchemy.domain.custom_serializer_mixin import CustomSerializerMixin
from src.sql_alchemy.domain.sql_alchemy import Base


class Account(Base, CustomSerializerMixin):
    __tablename__ = 'account'
    account_seq: int = Column(Integer, primary_key=True, comment='회원 일렬번호')
    account_email: str = Column(String(30), comment='회원 이메일')
    account_username: str = Column(String(50), comment='회원 이름')
    account_pw: str = Column(String(50), comment='회원 비밀번호')
    udid: str = Column(String(30), comment='핸드폰 고유번호')
    profile_seq: int = Column(Integer, ForeignKey('profile.profile_seq'), comment='프로필 일렬번호')
    site: str = Column(String(100), comment='회원 자동화 사이트')
    last_action_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='회원 마지막 행동 시간')
    reg_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='생성 시간')
    update_date: datetime = Column(DateTime, nullable=False, default=datetime.now(), comment='수정 시간')

    profile = relationship('Profile', back_populates="account", lazy="joined")
    tag_associations: list[AccountTagAssociation] = relationship(
        'AccountTagAssociation', lazy='joined', foreign_keys='AccountTagAssociation.account_seq')
    account_twitter_info: AccountTwitterInfo = relationship(
        'AccountTwitterInfo', back_populates="account", lazy="joined", uselist=False)

    def __init__(self,
                 account_seq: int = None,
                 account_email: str = None,
                 account_username: str = None,
                 account_pw: str = None,
                 udid: str = None,
                 profile_seq: int = None,
                 site: str = None,
                 profile: Profile = None,
                 last_action_date: datetime = None,
                 reg_date: datetime = None,
                 update_date: datetime = None
                 ):
        self.account_seq = account_seq
        self.account_email = account_email
        self.account_username = account_username
        self.account_pw = account_pw
        self.udid = udid
        self.profile_seq = profile_seq
        self.site = site
        self.profile = profile
        self.last_action_date = last_action_date

        if last_action_date is None:
            self.last_action_date = datetime.now()
        if reg_date is None:
            self.reg_date = datetime.now()
        if update_date is None:
            self.update_date = datetime.now()
