import os.path
from os import environ
from pathlib import Path
from dotenv import load_dotenv

# env 로드
load_dotenv(dotenv_path=os.path.join(os.getcwd(), Path('src/dot_env/env/datadog.env')))


# env 에서 받아온 db 정보
class DatadogEnv:
    DD_API_KEY = 'DD_API_KEY'
    DD_APP_KEY = 'DD_APP_KEY'
    DD_SITE = 'DD_SITE'

    api_key = environ[DD_API_KEY]
    app_key = environ[DD_APP_KEY]
    site = environ[DD_SITE]
