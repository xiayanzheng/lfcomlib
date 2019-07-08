from functools import wraps
import logging


def logger(level, name=None, message=None, log_path=None, log_format=None):

    def decorate(func):
        log_name = name if name else func.__module__
        log_msg = message if message else func.__name__
        log = logging.getLogger(log_name)
        logging.basicConfig(filename=log_path, format=log_format, level=level)

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, log_msg)
            return func(*args, **kwargs)

        return wrapper

    return decorate
