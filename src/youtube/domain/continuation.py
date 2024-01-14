from src.utils.object.object_utils import find_key_by_name


class Continuation:
    token: str

    def __init__(self, content: dict):
        continuations = find_key_by_name(content, "continuationItemRenderer")
        self.token = find_key_by_name(continuations, 'token')
