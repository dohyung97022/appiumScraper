from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from src.sql_alchemy.domain.sql_alchemy import Base
from src.sql_alchemy.domain.custom_serializer_mixin import CustomSerializerMixin


class Phone(Base, CustomSerializerMixin):
    serialize_rules = (
        '-action_associations.action.macros',
        '-action_associations.action.child_action_associations',
        '-action_associations.action.parent_action_associations',
    )

    __tablename__ = 'phone'
    udid: str = Column(String(30), primary_key=True, comment='핸드폰 udid')
    model: str = Column(String(20), comment='모델명')

    action_associations = relationship('PhoneActionAssociation', lazy='joined', foreign_keys='PhoneActionAssociation.udid')

    def __init__(self,
                 udid: str = None,
                 model: str = None,
                 ):
        self.udid = udid
        self.model = model

    def get_action_association_of_seq(self, action_association_seq: int):
        if action_association_seq is None:
            return None
        return next(filter(lambda association: association.phone_action_association_seq == action_association_seq, self.action_associations), None)

    def get_action_associations_not_in_seqs(self, action_association_seqs: list[int]):
        return list(filter(lambda association: association.phone_action_association_seq not in action_association_seqs, self.action_associations))

    @classmethod
    def get_action_association_seqs_of_json(cls, phone_action_associations_json: list[dict]):
        action_association_seqs = list(map(lambda association_json: association_json['phone_action_association_seq'], phone_action_associations_json))
        return list(filter(lambda action_association_seq: action_association_seq is not None, action_association_seqs))
