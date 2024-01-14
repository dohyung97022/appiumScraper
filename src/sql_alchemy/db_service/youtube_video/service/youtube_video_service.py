from sqlalchemy import insert

from src.sql_alchemy.db_model.youtube_video import YoutubeVideo
from src.sql_alchemy.service import db_session_service


def insert_youtube_video(video: YoutubeVideo):
    session = db_session_service.get_session()
    query = insert(YoutubeVideo).values([video.to_dict(rules=('-account_twitter_post',))]).prefix_with('IGNORE')
    session.execute(query)
    session.commit()
