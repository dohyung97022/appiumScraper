from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.sql_alchemy.db_model.tag import Tag
from src.sql_alchemy.domain.custom_serializer_mixin import CustomSerializerMixin
from src.sql_alchemy.domain.sql_alchemy import Base


class AccountTagAssociation(Base, CustomSerializerMixin):
    __tablename__ = 'account_tag_association'
    account_tag_association_seq: int = Column(Integer, primary_key=True, comment='계정, 태그 관계 테이블 일렬번호')

    account_seq: int = Column(Integer, ForeignKey('account.account_seq'), nullable=False, comment='계정 일렬번호')
    tag_seq: int = Column(Integer, ForeignKey('tag.tag_seq'), nullable=False, comment='태그 일렬번호')

    account = relationship('Account', foreign_keys=account_seq, lazy="noload", overlaps="tag_associations")
    tag = relationship('Tag', foreign_keys=tag_seq, lazy="joined")

    def __init__(self,
                 account_tag_association_seq: int = None,
                 account_seq: int = None,
                 tag_seq: int = None,
                 account=None,
                 tag: Tag = None,
                 ):
        self.account_tag_association_seq = account_tag_association_seq
        self.account_seq = account_seq
        self.tag_seq = tag_seq

        if account is not None:
            self.apply_account(account)
        if tag is not None:
            self.apply_tag(tag)

    def apply_account(self, account):
        self.account = account
        self.account_seq = account.account_seq

    def apply_tag(self, tag: Tag):
        self.tag = tag
        self.tag_seq = tag.tag_seq
