import functools
import platform
from lfcomlib.Jessica import DaPr
if platform.system() == 'Windows':
    import win32evtlog


class GetWindowsEventLog:

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

    def process_win_event_log(self, events, start, end, print_event_item=False, event_filter=None,
                              enable_message=False):
        package = []
        event_filter_x = []
        # print(event_filter_x)
        if event_filter is None:
            for k, v in self.event_dict:
                event_filter_x.append(v)
        elif type(event_filter) is list:
            for item in event_filter:
                event_filter_x.append(self.event_dict[item])

        timestamp_start = DaPr.datetime_to_timestamp(DaPr.string_to_datetime(start))
        timestamp_end = DaPr.datetime_to_timestamp(DaPr.string_to_datetime(end))
        for event in events:
            # print(event.TimeGenerated,event.SourceName)
            timestamp_event_time = DaPr.datetime_to_timestamp(
                event.TimeGenerated)
            if timestamp_start < timestamp_event_time > timestamp_end:
                # print(start, event.TimeGenerated, end)
                data_set = {
                    self.item_category: event.EventCategory,
                    self.item_time: event.TimeGenerated,
                    self.item_source_name: event.SourceName,
                    self.item_id: str(event.EventID),
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

    def get_event_data(self, server, event_channel, start, end, print_event_item=False, event_filter=None,
                       enable_message=False):
        channels = []
        processed_data = []
        if type(event_channel) is not list:
            channels.append(event_channel)
        elif type(event_channel) is list:
            channels = event_channel
        else:
            raise TypeError
        for channel in channels:
            core, flags = self.gen_event_log_core(server, channel)
            event_log_data = self.get_win_event_log(core, flags)
            single_channel_data = self.process_win_event_log(event_log_data, start, end, print_event_item, event_filter,
                                                             enable_message)
            processed_data.append(single_channel_data)
        processed_data = DaPr.merge_lists(processed_data)
        return processed_data


class GetWindowsEventLogByWmiQuery:

    def __init__(self):
        import wmi
        self.evt_type_code_dict = {
            "error": 1,
            "warning": 2,
            "information": 3,
            "security_audit_success": 4,
            "security_audit_failure": 5
        }
        self.wmi_intense = wmi.WMI()  # can put other server here if needed
        self.type_INFO = 3
        self.type_WARNING = 2
        self.type_ERROR = 1
        self.type_AUDIT_SUCCESS = 4
        self.type_AUDIT_FAILURE = 5
        self.evt_item_Category = 'Category'
        self.evt_item_ComputerName = 'ComputerName'
        self.evt_item_EventCode = 'EventCode'
        self.evt_item_EventIdentifier = 'EventIdentifier'
        self.evt_item_EventType = 'EventType'
        self.evt_item_InsertionStrings = 'InsertionStrings'
        self.evt_item_Logfile = 'Logfile'
        self.evt_item_Message = 'Message'
        self.evt_item_Environment = 'Environment'
        self.evt_item_RecordNumber = 'RecordNumber'
        self.evt_item_SourceName = 'SourceName'
        self.evt_item_TimeGenerated = 'TimeGenerated'
        self.evt_item_TimeWritten = 'TimeWritten'
        self.evt_item_Type = 'Type'
        self.evt_item_All = '*'
        self.disable_insertion_strings = True
        self.disable_data = True
        self.disable_message = True
        self.wql_set = {
            'wql_get_event_log_base': "SELECT {} FROM Win32_NTLogEvent ",
            'wql_get_event_log_logfile': '',
            'wql_get_event_log_evt_type': '',
            'wql_get_event_log_logfile_head': "WHERE Logfile='{}' ",
            "wql_get_event_log_logfile_extra": "OR Logfile='{}' ",
            'wql_get_event_log_time_range_start': "AND TimeWritten >= {} ",
            'wql_get_event_log_time_range_end': "AND TimeWritten < {} ",
            'wql_get_event_log_evt_single_type': "AND EventType={} ",
            'wql_get_event_log_evt_multi_type_front': "AND (EventType={} ",
            'wql_get_event_log_evt_multi_type_middle': "EventType={} ",
            'wql_get_event_log_evt_multi_type_back': "OR EventType={}) "
        }

    def set_evt_date_range(self, start_date, end_date):
        wql_list = []
        dates = [start_date, end_date]
        for i in range(len(dates)):
            data = dates[i]
            marks = ['/', '-']
            if type(dates[i]) is str:
                for mark in marks:
                    if mark in data:
                        dates[i] = functools.reduce(lambda x, y: x + y, dates[i].split(mark))

        wql_date_format = "'{}000000.000000-360'"
        times = [
            {"wql": self.wql_set["wql_get_event_log_time_range_start"], "param": wql_date_format.format(dates[0])},
            {"wql": self.wql_set["wql_get_event_log_time_range_end"], "param": wql_date_format.format(dates[1])},
        ]
        for wql_t in times:
            wql_list.append(wql_t['wql'].format(wql_t['param']))
        return wql_list

    def set_evt_log_file(self, cfg):
        wql_list = []
        param = cfg['param']
        wql_list.append(self.wql_set['wql_get_event_log_logfile_head'].format(param))
        wql_list.append(self.wql_set[cfg['wql']].format(cfg['param']))
        return wql_list

    def set_evt_log_type(self, cfg_set):
        wql_list = []
        type_list = cfg_set['param']
        for i in range(len(type_list)):
            type_i = type_list[i]
            if type(type_i) is str:
                n_type_i = str.lower(type_i)
                if n_type_i in self.evt_type_code_dict.keys():
                    type_list[i] = self.evt_type_code_dict[n_type_i]
        wql_list.append(self.wql_set['wql_get_event_log_evt_multi_type_front'].format(type_list[0]))
        if len(type_list) < 2:
            type_list.pop(0)
            for cfg in type_list:
                wql_list.append(self.wql_set['wql_get_event_log_evt_multi_type_middle'].format(cfg))
            wql_list.pop(-1)
        wql_list.append(self.wql_set['wql_get_event_log_evt_multi_type_back'].format(type_list[-1]))
        return wql_list

    def make_wql(self, cfg_set, start_date, end_date):
        wql_list = []
        for cfg in cfg_set:
            if cfg['wql'] == 'wql_get_event_log_base':
                wql_list.append(self.wql_set['wql_get_event_log_base'].format(cfg['param']))
            elif cfg['wql'] == 'wql_get_event_log_logfile':
                wql_list.extend(self.set_evt_log_file(cfg))
            elif cfg['wql'] == 'wql_get_event_log_evt_type':
                wql_list.extend(self.set_evt_log_type(cfg))
            elif cfg['wql'] in self.wql_set.keys():
                wql_list.append(self.wql_set[cfg['wql']].format(cfg['param']))
            else:
                wql_list.append(cfg['wql'].format(cfg['param']))
        wql_list.extend(self.set_evt_date_range(start_date, end_date))
        wql = functools.reduce(lambda x, y: x + y, wql_list)
        return wql

    def get_log(self, cfg_set, start_date, end_date, show_output=False):
        res = []
        for log_file in cfg_set['log_file']:
            new_cfg = [
                {"wql": "wql_get_event_log_base", "param": cfg_set['event_items']},
                {"wql": "wql_get_event_log_logfile", "param": log_file},
                {"wql": "wql_get_event_log_evt_type", "param": cfg_set['EventTypes']}
            ]
            wql = self.make_wql(new_cfg, start_date, end_date)
            if show_output:
                print(wql)
            evt_raw = self.wmi_intense.query(wql)

            for evt_log in evt_raw:
                if show_output:
                    print(evt_log)
                pkg = {}
                for attr in list(evt_log.__dict__['properties'].keys()):
                    if hasattr(evt_log, attr):
                        if str(attr) == 'InsertionStrings' and self.disable_insertion_strings:
                            pass
                        elif str(attr) == 'Data' and self.disable_data:
                            pass
                        elif str(attr) == 'Message' and self.disable_message:
                            pass
                        else:
                            pkg[attr] = str(getattr(evt_log, attr))
                res.append(pkg)
        return res
