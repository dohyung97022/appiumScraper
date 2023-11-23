import enum

from sqlalchemy import Column, Integer, String, Enum
from src.sql_alchemy.domain.sql_alchemy import Base
from src.sql_alchemy.domain.custom_serializer_mixin import CustomSerializerMixin


class ProxyState(enum.Enum):
    OPEN = 'OPEN'
    USED = 'USED'
    DISABLED = 'DISABLED'


class ProxyType(enum.Enum):
    LTE = 'LTE'
    USB_TETHERING = 'USB_TETHERING'
    HOTSPOT = 'HOTSPOT'
    NONE = 'NONE'


class Proxy(Base, CustomSerializerMixin):
    serialize_rules = ('-actions',)

    __tablename__ = 'proxy'
    proxy_seq: int = Column(Integer, primary_key=True, comment='프록시 일렬번호')
    udid: str = Column(String(30), comment='핸드폰 고유번호')
    hotspot_name: str = Column(String(30), comment='핸드폰 핫스팟 명칭')
    server: str = Column(String(100), comment='프록시 서버')
    port: int = Column(Integer, comment='프록시 포트')
    control_port: int = Column(Integer, comment='프록시 설정 요청용 포트')
    type: ProxyType = Column(Enum(ProxyType), nullable=False, default=ProxyType.NONE, comment='프록시 타입')
    state: ProxyState = Column(Enum(ProxyState), nullable=False, default=ProxyState.OPEN, comment='프록시 상태')
    user: str = Column(String(30), comment='프록시 사용자')

    def __init__(self,
                 proxy_seq: int = None,
                 server: str = None,
                 port: int = None,
                 control_port: int = None,
                 state: ProxyState = None,
                 user: str = None,
                 ):
        self.proxy_seq = proxy_seq
        self.server = server
        self.port = port
        self.control_port = control_port
        self.state = state
        self.user = user
