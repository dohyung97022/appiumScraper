from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from src.sql_alchemy.domain.custom_serializer_mixin import CustomSerializerMixin
from src.sql_alchemy.db_model.action import Action
from src.sql_alchemy.db_model.phone import Phone
from src.sql_alchemy.domain.sql_alchemy import Base


class PhoneActionAssociation(Base, CustomSerializerMixin):
    __tablename__ = 'phone_action_association'
    phone_action_association_seq: int = Column(Integer, primary_key=True, comment='핸드폰, 행동 관계 테이블 일렬번호')

    udid: str = Column(String(30), ForeignKey('phone.udid'), comment='핸드폰 udid')
    action_seq: int = Column(Integer, ForeignKey('action.action_seq'), comment='행동 일렬번호')

    phone = relationship('Phone', foreign_keys=udid, lazy="noload", overlaps="action_associations")
    action = relationship('Action', foreign_keys=action_seq, lazy="joined")

    def __init__(self,
                 phone_action_association_seq: int = None,
                 udid: str = None,
                 action_seq: int = None,
                 phone: Phone = None,
                 action: Action = None,
                 ):
        self.phone_action_association_seq = phone_action_association_seq
        self.udid = udid
        self.action_seq = action_seq

        if phone is not None:
            self.apply_phone(phone)
        if action is not None:
            self.apply_action(action)

    def apply_phone(self, phone: Phone):
        self.udid = phone.udid

    def apply_action(self, action: Action):
        self.action = action
        self.action_seq = action.action_seq

    def apply_json(self, json: dict):
        self.udid = json['udid']
        self.action_seq = json['action_seq']
