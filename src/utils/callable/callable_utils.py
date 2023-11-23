import time


def retry(function: callable, pass_if_fail: bool = False, retry: int = 20, *args, **kwarg):
    for i in range(retry):
        try:
            return function(*args, **kwarg)
        except:
            time.sleep(1)
    if not pass_if_fail:
        return function(*args, **kwarg)


def retry_until_success(function: callable, pass_if_fail: bool = False, retry: int = 30, *args, **kwarg):
    for i in range(retry):
        try:
            success = function(*args, **kwarg)
            if success:
                return
            time.sleep(1)
        except:
            time.sleep(1)
    if not pass_if_fail:
        raise Exception(f'retry failed. function : {function}, retry : {retry}')

