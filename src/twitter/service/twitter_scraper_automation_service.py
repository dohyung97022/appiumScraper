from datetime import datetime

from sqlalchemy.sql import functions
from tweety import Twitter
from tweety.exceptions_ import UserProtected, UserNotFound
from src.automation.account.service import user_service
from src.automation.tag.service import tag_service
from src.twitter.service import account_twitter_info_service
from src.sql_alchemy.db_model.account import Account
from src.sql_alchemy.db_model.account_twitter_info import AccountTwitterInfo
from src.sql_alchemy.service import db_session_service
from src.utils.callable import callable_utils
from src.utils.log import log_utils
from src.utils.log.log_utils import CustomLogger


class TwitterInfoStatisticsLogger(log_utils.CustomLogger):
    def __init__(self,
                 twitter_set_cnt: int,
                 fake_account_cnt: int,
                 followers_count_sum: int,
                 friends_count_sum: int
                 ):
        self.kwargs = {'extra': {'twitter': {'info': {}}}}
        self.kwargs['extra']['twitter']['info']['statistics'] = {
            'twitter_set_cnt': twitter_set_cnt,
            'fake_account_cnt': fake_account_cnt,
            'followers_count_sum': followers_count_sum,
            'friends_count_sum': friends_count_sum,
        }
        super(TwitterInfoStatisticsLogger, self).__init__()


def log_twitter_info_statistics():
    session = db_session_service.get_session()

    friends_count_sum, followers_count_sum = session.query(
        functions.sum(AccountTwitterInfo.friends_count),
        functions.sum(AccountTwitterInfo.followers_count),
        ).first()

    fake_account_cnt = session.query(
        functions.count()
        ).where(AccountTwitterInfo.profile_interstitial_type == 'fake_account')\
        .first()

    twitter_set_cnt = session.query(
        functions.count()
    ).where(AccountTwitterInfo.profile_interstitial_type == None) \
        .first()

    TwitterInfoStatisticsLogger(
        twitter_set_cnt=twitter_set_cnt[0],
        fake_account_cnt=fake_account_cnt[0],
        followers_count_sum=int(followers_count_sum),
        friends_count_sum=int(friends_count_sum)
    ).info('twitter info statistics.')


def scrape_user(account: Account):
    try:
        app = callable_utils.retry(Twitter, session_name="session", retry=3)
        user = callable_utils.retry(app.get_user_info, username=account.account_username, retry=3)
        # 비정상
        if user.profile_interstitial_type == 'fake_account':
            account_twitter_info_service.insert_update_account_banned(account)
            return
    # 비정상
    except (UserProtected, UserNotFound):
        account_twitter_info_service.insert_update_account_banned(account)
        return
    except KeyError as e:
        if 'guest_token' in str(e):
            CustomLogger().warn(
                message=f'scrape user failed. Rate limited. username : {account.account_username}', exception=e)
            return
        raise e
    # 실패
    except Exception as e:
        CustomLogger().error(message=f'scrape user failed. username : {account.account_username}', exception=e)
        return
    # 성공
    account_twitter_info_service.insert_save_account_twitter_info(account, user)


def loop_scrape_users(loop_range: int):
    tag = tag_service.select_or_create_tag_by_name('TWITTER_SET')
    for i in range(loop_range):
        account = user_service.select_user(order=AccountTwitterInfo.scrape_date, tags=[tag])
        account.account_twitter_info.scrape_date = datetime.now()
        account_twitter_info_service.insert_update_account_twitter_info(account.account_twitter_info)
        scrape_user(account)
    log_twitter_info_statistics()
