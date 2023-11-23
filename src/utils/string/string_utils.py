import re


def camel_case(string: str) -> str:
    string = re.sub(r"^[\-_\.]", '', string)
    return lower_case(string[0]) + re.sub(r"[\-_\.\s]([a-z\d])", lambda matched: upper_case(matched.group(1)), string[1:])


def lower_case(string: str) -> str:
    return str(string).lower()


def upper_case(string: str) -> str:
    return str(string).upper()


def space_to_underscore(string: str) -> str:
    return string.replace(' ', '_')


def get_between(string: str, after: str, prev: str, add_after_prev: bool = False) -> (bool, str):
    result = re.search(f'{after}(.*){prev}', string)
    if result is None:
        return False, None
    return True, f'{after}{result.group(1)}{prev}' if add_after_prev else result.group(1)


def get_before(string: str, before: str, add_before: bool = False) -> (bool, str):
    result = string.partition(before)[0]
    if result == '':
        return False, None
    return True, f'{result}{before}' if add_before else result


def get_after(string: str, after: str, add_after: bool = False) -> (bool, str):
    result = string.partition(after)[2]
    if result == '':
        return False, None
    return True, f'{after}{result}' if add_after else result


def remove_all(string: str, remove_list: list[str]) -> str:
    for remove_item in remove_list:
        string = string.replace(remove_item, '')
    return string
