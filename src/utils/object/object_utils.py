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


def find_keys_by_name(data, target_name, current_path=None):
    if current_path is None:
        current_path = []

    results = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_path = current_path + [key]
            results.extend(find_keys_by_name(value, target_name, new_path))
            if key == target_name:
                results.append(value)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_path = current_path + [index]
            results.extend(find_keys_by_name(item, target_name, new_path))

    return results


def find_key_by_name(data, target_name):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_name:
                return value
            found = find_key_by_name(value, target_name)
            if found is not None:
                return found
    elif isinstance(data, list):
        for index, item in enumerate(data):
            found = find_key_by_name(item, target_name)
            if found is not None:
                return found
    return None
