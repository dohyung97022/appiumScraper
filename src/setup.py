from pathlib import Path
from src.sql_alchemy.domain.sql_alchemy import db_setup
from src.utils.module import module_utils

db_model_path = Path("./src/sql_alchemy/db_model")
env_ends_with = 'env.py'


def configure():
    env_config()
    db_model_config()
    db_create_config()


# 모든 env import
def env_config():
    module_utils.import_all_modules_ends_with(env_ends_with)


# 모든 db model import
def db_model_config():
    module_utils.import_all_modules_in_folder(db_model_path)


# sql alchemy 데이터베이스 생성
def db_create_config():
    db_setup()
