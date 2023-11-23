from sqlalchemy import Column, Integer, String
from src.sql_alchemy.domain.sql_alchemy import Base
from src.sql_alchemy.domain.custom_serializer_mixin import CustomSerializerMixin


class Tag(Base, CustomSerializerMixin):
    __tablename__ = 'tag'
    tag_seq: int = Column(Integer, primary_key=True, comment='태그 일렬번호')
    name: str = Column(String(100), nullable=False, unique=True, comment='태그 이름')

    def __init__(self,
                 tag_seq: int = None,
                 name: str = None,
                 ):
        self.tag_seq = tag_seq
        self.name = name
