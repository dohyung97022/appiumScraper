from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from src.dot_env.domain.database_env import DatabaseEnv
import pymysql

# pymysql 로 MySQLdb 대체
pymysql.install_as_MySQLdb()

# 연결 설정
engine = create_engine(
    f'{DatabaseEnv.name}'
    f'://{DatabaseEnv.username}'
    f':{DatabaseEnv.password}'
    f'@{DatabaseEnv.endpoint}'
    f':{DatabaseEnv.port}'
    f'/{DatabaseEnv.schema}'
    f'?charset=utf8mb4',
    echo=False,
    pool_pre_ping=True,
    isolation_level="READ COMMITTED",
    )

# db 베이스
Base = declarative_base()


# db 에 생성 안된 테이블 생성
def db_setup():
    Base.metadata.create_all(engine)
