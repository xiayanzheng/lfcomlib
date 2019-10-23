from functools import wraps
import logging
from logging.handlers import RotatingFileHandler
import platform
from lfcomlib.Jessica.DaPr import DaPr

if platform.system() == 'Windows':
    from lfcomlib.Jessica import win32evtlog

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
            if level in self.log_level_dict:
                log_level = self.log_level_dict[level]
            log_file = "{}{}".format(log_path, '.log')
            log = logging.getLogger()
            log.setLevel(log_level)
            if len(log.handlers) == 0:
                # Log to file and console
                log_formatter = logging.Formatter(log_format)
                console = logging.StreamHandler()
                console.setLevel(log_level)
                console.setFormatter(log_formatter)
                log.addHandler(console)
                file = RotatingFileHandler(log_file, mode='a', maxBytes=int(log_size) * 1024 * 1024,
                                           backupCount=int(log_revision), encoding='utf-8', delay=0)
                file.setFormatter(log_formatter)
                file.setLevel(log_level)
                log.addHandler(file)
            log_set.log_core = log
            log_set.log_core_level = log_level


log_set = LogSet()


def logger():
    def decorate(func):
        if log_set.log_core is None:
            log_set.make_log_core(**log_cfg)
        message = ""
        log_core = log_set.log_core
        log_level = log_set.log_core_level

        @wraps(func)
        def wrapper(*args, **kwargs):
            log_msg_i = message if message else func.__name__
            func_obj = func(*args, **kwargs)
            if log_core is not None:
                try:
                    if log_level == logging.DEBUG:
                        try:
                            log_core.log(log_level, log_msg_i + "," + str(func_obj))
                        finally:
                            log_core.log(log_level, log_msg_i)
                    return func_obj
                except Exception as e:
                    log_msg_i = log_msg_i + str(e)
                    log_core.log(log_level, log_msg_i)
            else:
                return func_obj

        return wrapper

    return decorate


def logger_manual(*args):
    log_core = log_set.log_core
    log_level = logging.DEBUG
    if args[0] in log_set.log_level_dict:
        log_level = log_set.log_level_dict[args[0]]
    if log_core is None:
        log_set.make_log_core(**log_cfg)
    elif log_core is not None:
        log_core.log(log_level, str(args[1]))
    else:
        pass


class WindowsEventLog:

    def __init__(self):
        self.type_INFO = "EVENTLOG_INFORMATION_TYPE"
        self.type_WARNING = "EVENTLOG_WARNING_TYPE"
        self.type_ERROR = "EVENTLOG_ERROR_TYPE"
        self.type_AUDIT_SUCCESS = "EVENTLOG_AUDIT_SUCCESS"
        self.type_AUDIT_FAILURE = "EVENTLOG_AUDIT_FAILURE"
        self.event_dict = {
            'EVENTLOG_AUDIT_FAILURE': win32evtlog.EVENTLOG_AUDIT_FAILURE,
            'EVENTLOG_AUDIT_SUCCESS': win32evtlog.EVENTLOG_AUDIT_SUCCESS,
            'EVENTLOG_INFORMATION_TYPE': win32evtlog.EVENTLOG_INFORMATION_TYPE,
            'EVENTLOG_WARNING_TYPE': win32evtlog.EVENTLOG_WARNING_TYPE,
            'EVENTLOG_ERROR_TYPE': win32evtlog.EVENTLOG_ERROR_TYPE,
        }
        self.events_count = None
        self.item_category = "category"
        self.item_time = "time_generated"
        self.item_source_name = "source_name"
        self.item_id = "event_id"
        self.event_type = "event_type"
        self.event_message = "event_message"

    def gen_event_log_core(self, server, event_channel):
        core = win32evtlog.OpenEventLog(server, event_channel)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        return core, flags

    def get_win_event_log(self, log_core, flags):
        self.events_count = win32evtlog.GetNumberOfEventLogRecords(log_core)
        events = win32evtlog.ReadEventLog(log_core, flags, 0)
        return events

    def process_win_event_log(self, events, print_event_item=False, event_filter=None, enable_message=False):
        package = []
        event_filter_x = []
        print(event_filter_x)
        if event_filter is None:
            for k, v in self.event_dict:
                event_filter_x.append(v)
        elif type(event_filter) is list:
            for item in event_filter:
                event_filter_x.append(self.event_dict[item])
        for event in events:
            data_set = {
                self.item_category: event.EventCategory,
                self.item_time: event.TimeGenerated,
                self.item_source_name: event.SourceName,
                self.item_id: event.EventID,
                self.event_type: event.EventType,
                self.event_message: "disabled",
            }
            if enable_message:
                data_set[self.event_message] = event.StringInserts
            if event.EventType in event_filter_x:
                if print_event_item:
                    print(data_set)
                package.append(data_set)
        return package

    def get_event_data(self, server, event_channel, print_event_item=False, event_filter=None, enable_message=False):
        channels = []
        processed_data = None
        if type(event_channel) is not list:
            channels.append(event_channel)
        elif type(event_channel) is list:
            channels = event_channel
        else:
            raise TypeError
        for channel in channels:
            core, flags = self.gen_event_log_core(server, channel)
            event_log_data = self.get_win_event_log(core, flags)
            single_channel_data = self.process_win_event_log(event_log_data, print_event_item, event_filter,
                                                             enable_message)
            if processed_data is None:
                processed_data = single_channel_data
            processed_data.append(single_channel_data)
        processed_data = DaPr.merge_lists([], processed_data)
        return processed_data
