from sqlalchemy import text

from src.sql_alchemy.db_model.account import Account
from src.sql_alchemy.db_model.account_tag_association import AccountTagAssociation
from src.sql_alchemy.db_model.account_twitter_info import AccountTwitterInfo
from src.sql_alchemy.db_model.tag import Tag
from src.sql_alchemy.service import db_session_service


# 계정 저장
def insert_user(user: Account):
    session = db_session_service.get_session()
    session.add(user)
    session.commit()
    session.refresh(user)


# 계정 선택
def select_user_by_seq(seq: int) -> Account:
    return db_session_service.get_session().query(Account).get(seq)


def select_user(seq: int = None, where: str = None, email: str = None, site: str = None, tags: list[Tag] = None, order=None) -> Account:
    session = db_session_service.get_session()
    query = session.query(Account)
    if where:
        query = query.filter(text(where))
    if seq:
        query = query.filter(Account.account_seq == seq)
    if email:
        query = query.filter(Account.account_email == email)
    if site:
        query = query.filter(Account.site == site)
    if tags:
        for tag in tags:
            query = query.filter(Account.tag_associations.any(AccountTagAssociation.tag_seq == tag.tag_seq))
    if order:
        if order.class_ != Account:
            query = query.join(order.class_)

        query = query.order_by(order)
    return query.first()


def select_users(where: str = None, email: str = None, site: str = None, tags: list[Tag] = None, order=None) -> list[Account]:
    session = db_session_service.get_session()
    query = session.query(Account)
    if where:
        query = query.filter(text(where))
    if email:
        query = query.filter(Account.account_email == email)
    if site:
        query = query.filter(Account.site == site)
    if tags:
        for tag in tags:
            query = query.filter(Account.tag_associations.any(AccountTagAssociation.tag_seq == tag.tag_seq))
    if order:
        query = query.order_by(order)
    return query.all()


def update_user(account: Account):
    session = db_session_service.get_session()
    session.merge(account)
    session.commit()
