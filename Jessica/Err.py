from functools import wraps
import os, time
import logging


def logger(level, name=None, message=None, log_path=None, log_format=None):
    def decorate(func):
        log_level_dict = {
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        if level in log_level_dict:
            log_level = log_level_dict[level]
        else:
            log_level = logging.DEBUG
        log_name = name if name else func.__module__
        log_msg = message if message else func.__name__
        log = logging.getLogger(log_name)
        log_file = "{}_{}{}".format(log_path, time.strftime("%Y-%m-%d", time.localtime()), '.log')
        logging.basicConfig(filename=log_file, format=log_format, level=log_level)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        log.log(log_level, log_msg)
        return wrapper

    return decorate
