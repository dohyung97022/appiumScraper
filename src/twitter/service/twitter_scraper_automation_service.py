from datetime import datetime, timedelta

from sqlalchemy.sql import functions
from tweety import Twitter
from tweety.exceptions_ import UserProtected, UserNotFound

from src.sql_alchemy.db_model.account_twitter_post import AccountTwitterPost
from src.sql_alchemy.db_service.account.service import account_service
from src.sql_alchemy.db_service.account_twitter_post.service import account_twitter_post_service
from src.sql_alchemy.db_service.tag.service import tag_service
from src.twitter.service import account_twitter_info_service
from src.sql_alchemy.db_model.account import Account
from src.sql_alchemy.db_model.account_twitter_info import AccountTwitterInfo
from src.sql_alchemy.service import db_session_service
from src.twitter.service.account_twitter_info_service import TwitterRegisterStatisticsLogger
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


def insert_update_account_banned(account: Account):
    if account.reg_date > datetime.now() - timedelta(hours=3):
        TwitterRegisterStatisticsLogger('BANNED').info(message=f'twitter account creation banned.')
    tag_service.remove_account_tag_by_names(account, ['TWITTER_SET'])
    account.account_twitter_info.profile_interstitial_type = 'fake_account'
    account_twitter_info_service.insert_update_account_twitter_info(account.account_twitter_info)


def scrape_user(account: Account):
    try:
        app = callable_utils.retry(Twitter, session_name="session", retry=3)
        user = callable_utils.retry(app.get_user_info, username=account.account_username, retry=3)
        if user.profile_interstitial_type == 'fake_account':
            account_twitter_info_service.insert_update_account_banned(account)
            return
        account_twitter_info_service.insert_save_account_twitter_info(account, user)
    # 비정상
    except (UserProtected, UserNotFound):
        account_twitter_info_service.insert_update_account_banned(account)
    except KeyError as e:
        if 'guest_token' in str(e):
            CustomLogger().warn(
                message=f'scrape user failed. Rate limited. username : {account.account_username}', exception=e)
        else:
            CustomLogger().error(message=f'scrape user failed. username : {account.account_username}', exception=e)
    except Exception as e:
        CustomLogger().error(message=f'scrape user failed. username : {account.account_username}', exception=e)


def scrape_post(post: AccountTwitterPost):
    try:
        app = callable_utils.retry(Twitter, session_name="session", retry=3)
        tweet_detail = Twitter(app).tweet_detail(str(post.post_id))
        post.apply_tweet_detail(tweet_detail)
        post.update_date = datetime.now()
        account_twitter_post_service.insert_update_account_twitter_post(post)
    except Exception as e:
        CustomLogger().error(message=f'scrape post failed. post_id : {post.post_id}', exception=e)


def loop_scrape_users(loop_range: int):
    tag = tag_service.select_or_create_tag_by_name('TWITTER_SET')
    for i in range(loop_range):
        account = account_service.select_account(order=AccountTwitterInfo.scrape_date, tags=[tag])
        account.account_twitter_info.scrape_date = datetime.now()
        account_twitter_info_service.insert_update_account_twitter_info(account.account_twitter_info)
        scrape_user(account)
    log_twitter_info_statistics()


def loop_scrape_posts(loop_range: int):
    for i in range(loop_range):
        post = account_twitter_post_service.select_account_twitter_post(order=AccountTwitterPost.scrape_date)
        post.scrape_date = datetime.now()
        account_twitter_post_service.insert_update_account_twitter_post(post)
        scrape_post(post)
