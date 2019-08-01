from functools import wraps
import logging
from logging.handlers import RotatingFileHandler
from lfcomlib.Jessica import inspect

log_cfg = {}


class LogSet:
    def __init__(self):
        self.log_core = None
        self.log_core_level = None
        self.log_level_dict = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }

    def make_log_core(self, **kwargs):
        if kwargs:
            log_level = logging.DEBUG
            level = kwargs['log_level']
            log_path = kwargs['log_path']
            log_format = kwargs['log_format']
            log_revision = kwargs["log_revision"]
            log_size = kwargs["log_size"]
            set_level_every_time = False
            if 'set_level_every_time' in kwargs.keys():
                set_level_every_time = kwargs["set_level_every_time"]
            if level in self.log_level_dict.keys():
                log_level = self.log_level_dict[level]
            log_file = "{}{}".format(log_path, '.log')
            log = logging.getLogger()
            if len(log.handlers) == 0:
                # Log to file and console
                log_formatter = logging.Formatter(log_format)
                console = logging.StreamHandler()
                console.setLevel(log_level)
                console.setFormatter(log_formatter)
                log.addHandler(console)
                file = RotatingFileHandler(log_file, mode='a', maxBytes=int(log_size) * 1024 * 1024,
                                           backupCount=int(log_revision), encoding=None, delay=0)
                file.setFormatter(log_formatter)
                file.setLevel(log_level)
                log.addHandler(file)
            log_set.log_core = log
            log_set.log_core_level = log_level
            if set_level_every_time is True:
                return log


log_set = LogSet()


def logger():
    def decorate(func):
        if log_set.log_core is None:
            log_set.make_log_core(**log_cfg)
        message = ""
        log_core = log_set.log_core
        log_level = log_set.log_core_level
        # print(log_core.__dict__)

        @wraps(func)
        def wrapper(*args, **kwargs):
            log_msg_i = message if message else func.__name__
            func_name = inspect.stack()[1][3]
            log_msg_i = "{},{}".format(func_name, log_msg_i)
            func_obj = func(*args, **kwargs)
            if log_core is not None:
                try:
                    if log_level == logging.DEBUG:
                        log_core.log(log_level, log_msg_i)
                    return func_obj
                except Exception as e:
                    log_msg_i = log_msg_i + str(e)
                    log_core.log(log_level, log_msg_i)
            else:
                return func_obj

        return wrapper

    return decorate


def logger_i(*args, set_level_every_time=True,):
    fun_name = inspect.stack()[1][3]
    log_core = log_set.log_core
    log_level = logging.DEBUG
    if set_level_every_time is True:
        log_cfg['set_level_every_time'] = set_level_every_time
        log_cfg['log_level'] = args[0]
        log_core = log_set.make_log_core(**log_cfg)
    else:
        if args[0] in log_set.log_level_dict:
            log_level = log_set.log_level_dict[args[0]]
        if log_core is None:
            log_set.make_log_core(**log_cfg)
    if log_core is not None:
        log_core.log(log_level, "{},{}".format(fun_name, str(args[1])))
    else:
        pass
