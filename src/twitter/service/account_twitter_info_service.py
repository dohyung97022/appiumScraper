import datetime
from tweety.types import User
from src.automation.tag.service import tag_service
from src.sql_alchemy.db_model.account import Account
from src.sql_alchemy.db_model.account_tag_association import AccountTagAssociation
from src.sql_alchemy.db_model.account_twitter_info import AccountTwitterInfo
from src.sql_alchemy.db_model.tag import Tag
from src.sql_alchemy.service import db_session_service
from src.utils.log import log_utils


class TwitterRegisterStatisticsLogger(log_utils.CustomLogger):
    def __init__(self, status: str):
        self.kwargs = {'extra': {'twitter': {'info': {}}}}
        self.kwargs['extra']['twitter']['info']['register'] = {
            'status': status,
        }
        super(TwitterRegisterStatisticsLogger, self).__init__()


def select_account_twitter_info(account_seq: int = None, is_default_profile_image: bool = None) -> AccountTwitterInfo:
    session = db_session_service.get_session()
    query = session.query(AccountTwitterInfo)
    if account_seq is not None:
        query = query.filter(AccountTwitterInfo.account_seq == account_seq)
    if is_default_profile_image is not None:
        query = query.filter(AccountTwitterInfo.is_default_profile_image == is_default_profile_image)

    return query.first()


def select_account_twitter_info_of_tag_order_of_scrape_date(tags: list[Tag] = None):
    session = db_session_service.get_session()
    query = session.query(Account)
    query = query.join(AccountTwitterInfo)

    if tags:
        for tag in tags:
            query = query.filter(Account.tag_associations.any(AccountTagAssociation.tag_seq == tag.tag_seq))

    query = query.order_by(AccountTwitterInfo.scrape_date)
    return query.first()


def insert_update_account_twitter_info(account_twitter_info: AccountTwitterInfo):
    session = db_session_service.get_session()
    session.merge(account_twitter_info)
    session.commit()


def insert_save_account_twitter_info(account: Account, user: User):
    # account_twitter_info 저장
    account_twitter_info = select_account_twitter_info(account.account_seq)
    if account_twitter_info is None:
        account_twitter_info = AccountTwitterInfo(account_seq=account.account_seq)
    account_twitter_info.update_date = datetime.datetime.now()
    account_twitter_info.apply_user(user)
    insert_update_account_twitter_info(account_twitter_info)


def insert_update_account_banned(account: Account):

    if account.reg_date > datetime.datetime.now() - datetime.timedelta(hours=3):
        TwitterRegisterStatisticsLogger('BANNED').info(message=f'twitter account creation banned.')
    tag_service.remove_account_tag_by_names(account, ['TWITTER_SET'])
    twitter_info = select_account_twitter_info(account_seq=account.account_seq)
    if twitter_info is None:
        twitter_info = AccountTwitterInfo(account_seq=account.account_seq)
    twitter_info.update_date = datetime.datetime.now()
    twitter_info.profile_interstitial_type = 'fake_account'
    insert_update_account_twitter_info(twitter_info)
