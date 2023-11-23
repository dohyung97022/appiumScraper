import enum

from sqlalchemy import Column, Integer, Enum, String, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from src.sql_alchemy.domain.custom_serializer_mixin import CustomSerializerMixin
from src.sql_alchemy.domain.sql_alchemy import Base


class ElementType(enum.Enum):
    ID = "ID"
    XPATH = "XPATH"
    LINK_TEXT = "LINK_TEXT"
    PARTIAL_LINK_TEXT = "PARTIAL_LINK_TEXT"
    NAME = "NAME"
    TAG_NAME = "TAG_NAME"
    CLASS_NAME = "CLASS_NAME"
    CSS_SELECTOR = "CSS_SELECTOR"


class Element(Base, CustomSerializerMixin):
    serialize_rules = ('-macro',)

    __tablename__ = 'element'
    element_seq: int = Column(Integer, primary_key=True, comment='element 일렬번호')
    macro_seq: int = Column(Integer, ForeignKey("macro.macro_seq"), nullable=False, comment='macro 일렬번호')
    value: str = Column(String(500), nullable=False)
    index: int = Column(SmallInteger, nullable=False, default=0, comment='element 조회 인덱스, -1 일 경우 random')
    type: ElementType = Column(Enum(ElementType), nullable=False, default=ElementType.XPATH, comment='element 종류')
    order: int = Column(SmallInteger, nullable=False, default=0, comment='element 탐색 순서')

    macro = relationship("Macro", back_populates="elements", lazy="noload")

    def __init__(self,
                 element_seq: int = None,
                 macro_seq: int = None,
                 value: str = None,
                 index: int = None,
                 type: ElementType = None,
                 order: int = None,
                 element_json: dict = None
                 ):
        self.element_seq = element_seq
        self.macro_seq = macro_seq
        self.value = value
        self.index = index
        self.type = type
        self.order = order

        if element_json is not None:
            self.apply_json(element_json)

    def apply_json(self, element_json: dict):
        self.element_seq = element_json['element_seq']
        self.macro_seq = element_json['macro_seq']
        self.value = element_json['value']
        self.index = element_json['index']
        self.type = ElementType[element_json['type']]
        self.order = element_json['order']
