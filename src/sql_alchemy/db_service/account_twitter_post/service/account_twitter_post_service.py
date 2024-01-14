from sqlalchemy import text
from src.sql_alchemy.db_model.account_twitter_post import AccountTwitterPost
from src.sql_alchemy.service import db_session_service


def select_account_twitter_post(seq: int = None, where: str = None, order=None) -> AccountTwitterPost:
    session = db_session_service.get_session()
    query = session.query(AccountTwitterPost)
    if where:
        query = query.filter(text(where))
    if seq:
        query = query.filter(AccountTwitterPost.account_twitter_post_seq == seq)
    if order:
        if order.class_ != AccountTwitterPost:
            query = query.join(order.class_)
        query = query.order_by(order)
    return query.first()


def insert_update_account_twitter_post(account_twitter_post: AccountTwitterPost):
    session = db_session_service.get_session()
    session.merge(account_twitter_post)
    session.commit()
