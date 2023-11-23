import inspect


def is_match_of_types(obj, types: tuple):
    if not inspect.isclass(obj):
        return False

    is_match: bool = True
    for matching_type in types:
        is_match = issubclass(obj, matching_type)
        if not is_match:
            break

    return is_match
