from datetime import datetime

from src.sql_alchemy.db_service.account.common.faker_sex import FakerSex


class FakerProfile:
    username: str
    name: str
    sex: FakerSex
    birthdate: datetime
    address: str
    email: str
    password: str

    def __init__(self, profile_dict: dict):
        self.username = profile_dict['username']
        self.name = profile_dict['name']
        self.sex = FakerSex(profile_dict['sex'])
        self.birthdate = profile_dict['birthdate']
        self.address = profile_dict['address']
