from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.sql_alchemy.domain.custom_serializer_mixin import CustomSerializerMixin
from src.sql_alchemy.db_model.action import Action
from src.sql_alchemy.domain.sql_alchemy import Base


class ActionActionAssociation(Base, CustomSerializerMixin):
    __tablename__ = 'action_action_association'
    action_action_association_seq: int = Column(Integer, primary_key=True, comment='행동 관계 테이블 일렬번호')
    association_order: int = Column(Integer, comment='관계 동작 순서')

    child_action_seq: int = Column(Integer, ForeignKey('action.action_seq'), comment='자식 행동 일렬번호')
    parent_action_seq: int = Column(Integer, ForeignKey('action.action_seq'), comment='부모 행동 일렬번호')

    child_action = relationship('Action', foreign_keys=child_action_seq, lazy="joined", overlaps="parent_action_associations")
    parent_action = relationship('Action', foreign_keys=parent_action_seq, lazy="noload", overlaps="child_action_associations")

    def __init__(self,
                 action_action_association_seq: int = None,
                 association_order: int = None,
                 child_action_seq: int = None,
                 parent_action_seq: int = None,
                 parent_action: Action = None,
                 child_action: Action = None
                 ):
        self.action_action_association_seq = action_action_association_seq
        self.association_order = association_order
        self.child_action_seq = child_action_seq
        self.parent_action_seq = parent_action_seq

        if parent_action is not None:
            self.apply_parent_action(parent_action)
        if child_action is not None:
            self.apply_child_action(child_action)

    def apply_parent_action(self, parent_action: Action):
        self.parent_action_seq = parent_action.action_seq
        self.parent_action = parent_action

    def apply_child_action(self, child_action: Action):
        self.child_action_seq = child_action.action_seq
        self.child_action = child_action
