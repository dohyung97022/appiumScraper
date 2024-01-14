from src.utils.object.object_utils import find_key_by_name, find_keys_by_name


class Chip:
    name_to_token: dict = {}

    def __init__(self, content):
        chips = find_keys_by_name(content, "chipCloudChipRenderer")
        for content in chips:
            self.name_to_token[find_key_by_name(content, "simpleText")] = find_key_by_name(content, "token")
