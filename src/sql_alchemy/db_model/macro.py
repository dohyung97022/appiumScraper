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


class MacroType(enum.Enum):
    CLICK = 'CLICK'
    PYAUTOGUI_CLICK = 'PYAUTOGUI_CLICK'
    SWITCH_TO_FRAME = 'SWITCH_TO_FRAME'
    SWITCH_TO_DEFAULT = 'SWITCH_TO_DEFAULT'
    DRAG = 'DRAG'
    SCROLL = 'SCROLL'
    RUN = 'RUN'
    TYPE = 'TYPE'
    TYPE_CLEAR = 'TYPE_CLEAR'
    ERROR = 'ERROR'
    BOOT = 'BOOT'
    STOP = 'STOP'
    RECORD = 'RECORD'


class DriverType(enum.Enum):
    APP = 'APP'
    WEB = 'WEB'
    UNDETECTED_CHROME = 'UNDETECTED_CHROME'


class MacroOperator(enum.Enum):
    NONE = 'NONE'
    TRY = 'TRY'
    OR = 'OR'
    FAIL_END = 'FAIL_END'


class Macro(Base, CustomSerializerMixin):
    serialize_rules = ('-action',)

    # db 저장 내용
    __tablename__ = 'macro'
    macro_seq: int = Column(Integer, primary_key=True, comment='매크로 일렬번호')
    action_seq: int = Column(Integer, ForeignKey("action.action_seq"))
    name: str = Column(String(100), comment='매크로 이름')
    driver_type: DriverType = Column(Enum(DriverType), comment='매크로 적용 driver 종류')
    element_type: ElementType = Column(Enum(ElementType), comment='매크로 적용 element 종류')
    element: str = Column(String(500), comment='element 식별자')
    function_name: str = Column(String(100), comment='macro_type.RUN 의 function 이름')
    variable: str = Column(String(500), comment='변수, MacroType.TYPE: 입력값, MacroType.RUN: 변수값')
    macro_type: MacroType = Column(Enum(MacroType), comment='매크로 종류')
    macro_index: int = Column(Integer, comment='매크로 적용할 인덱스, -1일 경우 random')
    macro_weight: int = Column(Integer, nullable=False, default=0, comment='매크로 실행 확률')
    macro_operator: MacroOperator = Column(Enum(MacroOperator), comment='매크로 실행조건')
    min_wait_sec: int = Column(Integer, comment='매크로 적용 최소 대기시간')
    max_wait_sec: int = Column(Integer, comment='매크로 적용 최대 대기시간')
    repeat_times: int = Column(SmallInteger, nullable=False, default=0, comment='반복 횟수')
    retry_times: int = Column(Integer, comment='매크로 재시도 횟수')
    retry_wait_sec: int = Column(Integer, comment='매크로 재시도 대기시간')
    macro_order: int = Column(Integer, comment='매크로 동작 순서')

    action = relationship("Action", back_populates="macros", lazy="noload")
    elements = relationship("Element", back_populates="macro", lazy="joined", order_by="Element.order")

    def __init__(self,
                 macro_seq: int = None,
                 action_seq: int = None,
                 name: str = None,
                 driver_type: DriverType = None,
                 element_type: ElementType = None,
                 element: str = None,
                 function_name: str = None,
                 variable: str = None,
                 macro_type: MacroType = None,
                 macro_index: int = None,
                 macro_weight: int = None,
                 macro_operator: MacroOperator = None,
                 min_wait_sec: int = None,
                 max_wait_sec: int = None,
                 repeat_times: int = None,
                 retry_times: int = None,
                 retry_wait_sec: int = None,
                 macro_order: int = None,
                 macro_json: dict = None
                 ):
        self.macro_seq = macro_seq
        self.action_seq = action_seq
        self.name = name
        self.driver_type = driver_type
        self.element_type = element_type
        self.element = element
        self.function_name = function_name
        self.variable = variable
        self.macro_type = macro_type
        self.macro_index = macro_index
        self.macro_weight = macro_weight
        self.macro_operator = macro_operator
        self.min_wait_sec = min_wait_sec
        self.max_wait_sec = max_wait_sec
        self.repeat_times = repeat_times
        self.retry_times = retry_times
        self.retry_wait_sec = retry_wait_sec
        self.macro_order = macro_order

        if macro_json is not None:
            self.apply_json(macro_json)

    def apply_json(self, macro_json: dict):
        self.macro_seq = macro_json['macro_seq']
        self.action_seq = macro_json['action_seq']
        self.name = macro_json['name']
        self.driver_type = DriverType[macro_json['driver_type']]
        self.element_type = ElementType[macro_json['element_type']]
        self.element = macro_json['element']
        self.function_name = macro_json['function_name']
        self.variable = macro_json['variable']
        self.macro_type = MacroType[macro_json['macro_type']]
        self.macro_index = macro_json['macro_index']
        self.macro_weight = macro_json['macro_weight']
        self.macro_operator = MacroOperator[macro_json['macro_operator']]
        self.min_wait_sec = macro_json['min_wait_sec']
        self.max_wait_sec = macro_json['max_wait_sec']
        self.repeat_times = macro_json['repeat_times']
        self.retry_times = macro_json['retry_times']
        self.retry_wait_sec = macro_json['retry_wait_sec']
        self.macro_order = macro_json['macro_order']

    def get_element_of_seq(self, element_seq: int):
        if element_seq is None:
            return None
        return next(filter(lambda element: element.element_seq == element_seq, self.elements), None)

    def get_elements_not_in(self, element_seqs: list[int]):
        return list(filter(lambda element: element.element_seq not in element_seqs, self.elements))

    @classmethod
    def get_element_seqs_from_macro_json(cls, macro_json):
        return list(map(lambda element: element['element_seq'], macro_json['elements']))