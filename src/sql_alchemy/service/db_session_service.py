from multiprocessing import current_process

import sqlalchemy.exc
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from src.sql_alchemy.domain.sql_alchemy import engine

ScopedSession = scoped_session(sessionmaker(bind=engine))
process_session: Session | None = None


def create_session():
    # process 일 경우
    if current_process().name != 'MainProcess':
        global process_session
        process_session = sessionmaker(bind=engine)()
    # 직접 생성된 thread 일 경우
    global ScopedSession
    ScopedSession = scoped_session(sessionmaker(bind=engine))


def close_session():
    try:
        # process 일 경우
        if current_process().name != 'MainProcess':
            global process_session
            process_session.close()
            return
        # 직접 생성된 thread 일 경우
        global ScopedSession
        ScopedSession.close()
    except sqlalchemy.exc.OperationalError as e:
        if 'Server has gone away' in str(e) or 'Lost connection to MySQL server' in str(e):
            return
        raise e
    except Exception as e:
        raise e


def get_session() -> Session:
    # 직접 생성된 process 일 경우
    if current_process().name != 'MainProcess':
        global process_session
        return process_session
    # 직접 생성된 thread 일 경우
    return ScopedSession()
