from lfcomlib.Jessica import os, time, datetime, reduce, re


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


class Core:

    @staticmethod
    def find_path_backward(init_path, target, max_layer=30):
        pre = '..'
        p = [init_path]
        f = os.path.abspath(os.path.join(*p))
        rr = os.path.join(f, target)
        sk = os.path.exists(rr)
        counter = 0
        while sk is not True and counter < max_layer:
            p.append(pre)
            f = os.path.abspath(os.path.join(*p))
            rr = os.path.abspath(os.path.join(f, target))
            sk = os.path.exists(rr)
            counter += 1
            if counter == max_layer:
                break
        if counter == max_layer:
            return None
        return rr

    def tuple_list_to_list(self, tuple_list):
        list = []
        for tuple in tuple_list:
            list.append(tuple[0])
        return list

    def find_diff_value_from_two_dicts(self, type_i, origi, modified):
        if type_i in ['dict', 'Dict']:
            diff = {}
            for Key, Value in origi.items():
                try:
                    if modified[Key] == Value:
                        pass
                    else:
                        diff[Key] = Value
                except:
                    pass
            return diff

    @staticmethod
    def keep_one(raw_data):
        keep_one = []
        package = []
        for Data in raw_data:
            if Data not in keep_one:
                keep_one.append(Data)
                package.append({'value': Data, 'label': Data})
            else:
                pass
        keep_one.clear()
        return package

    @staticmethod
    def find_newest_file_in_windows(user_dir, file_extension_list):
        file_list = []
        for Files in os.walk(user_dir):
            for FileName in Files[2]:
                if FileName.split(".")[-1] in file_extension_list:
                    FilePath = os.path.join(Files[0], FileName)
                    file_list.append((FileName, os.path.getctime(FilePath), FilePath))
        if len(file_list) > 1:
            return sorted(file_list, key=lambda FileCreateTime: FileCreateTime[1])[-1][2]
        else:
            return False

    @staticmethod
    def match_datetime_from_str(data):
        reg = "([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-" \
              "(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))\s(" \
              "[0-1][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])"
        result = re.search(reg, data)
        if result is not None:
            return result.group()
        else:
            return None

    def replace_dir_slash(self, user_dir):
        return reduce(lambda x, y: x + y, self.insert_values_to_list(user_dir.split("/"), "\\"))

    def replace_dir_symbol(self, user_dir, replace_from, replace_to):
        return reduce(lambda x, y: x + y, self.insert_values_to_list(user_dir.split(replace_from), replace_to))

    def replace_symbol(self, user_str, replace_from, replace_to):
        return reduce(lambda x, y: x + y, self.insert_values_to_list(user_str.split(replace_from), replace_to))

    def clean_list(self, str_i, split_str, *args):
        raw = str_i.split(split_str)
        new = []
        for x in raw:
            if x not in args:
                new.append(x)
        return new

    def gen_path(self, drive, list_s):
        drive_l = [drive]
        list_n = drive_l + list_s
        path = os.path.join(*list_n)
        return path

    def insert_value_to_list_and_merge(self, u_list, value):
        return reduce(lambda x, y: x + y, self.insert_values_to_list(u_list, value))

    def rename_dict_keys(self, raw_data, replace_key_map):
        for Key in raw_data:
            for RDKey, RDVaule in replace_key_map.items():
                if Key == RDKey:
                    raw_data[RDVaule] = raw_data.pop(Key)
        return raw_data

    def insert_values_to_list(self, data_set, insert_value):
        union_data = []
        if isinstance(data_set, list):
            for Data in data_set:
                union_data.append(Data)
                union_data.append(insert_value)
            del union_data[-1]
            return union_data
        else:
            return data_set

    def insert_into_x_values_to_list(self, data_set, gap, insert_value):
        union_data = []
        count = 0
        if len(data_set) > gap:
            for Data in data_set:
                if count < gap:
                    union_data.append(Data)
                    count += 1
                else:
                    union_data.append(insert_value)
                    count = 0
            del union_data[-1]
        else:
            for Data in data_set:
                union_data.append(Data)
        return union_data

    def unpackage_list_and_insert_values_to_list(self, data_set, insert_value):
        union_data = []
        for List in data_set:
            for Data in List:
                union_data.append(Data)
            union_data.append(insert_value)
        del union_data[-1]
        return union_data

    def merge_multi_tuple_list(self, tuple_list):
        raw_list = []
        for Tuple in tuple_list:
            for Data in Tuple:
                raw_list.append(Data)
        return raw_list

    def merge_lists(self, data_list, *args):
        base = ["place_holder"]
        for data in data_list:
            base.extend(data)
        if len(args) != 0:
            for list_data in args:
                for list_item in list_data:
                    base.extend(list_item)
        base.pop(0)
        return base

    def merge_two_dicts(self, dict_a, dic_b):
        merged_dict = {}
        for Key, Value in dict_a.items():
            merged_dict[Key] = Value
        for Key, Value in dic_b.items():
            merged_dict[Key] = Value
        return merged_dict

    def find_valid_data_from_dict(self, valid_data_name, dict_i):
        valid_data = {}
        for Key, Value in dict_i.items():
            if Key in valid_data_name:
                valid_data[Key] = Value
        return valid_data

    def root_path(self, root_dir_name):
        init_path = os.getcwd()
        if '\\' in init_path:
            init_path = os.getcwd().split('\\')
        elif '/' in init_path:
            init_path = os.getcwd().split('/')
        temp = []
        for Folder in init_path:
            if Folder != root_dir_name:
                temp.append(Folder)
            else:
                temp.append(root_dir_name)
                break
        return reduce(lambda x, y: x + y, self.insert_values_to_list(temp, '\\'))

    def convert_two_lists_to_dict(self, list_for_key, list_for_value):
        new_dict = dict(zip(list_for_key, list_for_value))
        return new_dict

    def dedupe(self, dataset):
        package = []
        for Data in dataset:
            if Data not in package:
                package.append(Data)
            else:
                pass
        return package

    def timestamp_to_datetime(self, timestamp):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))

    def string_to_datetime(self, txt):
        if type(txt) is str:
            fmt = '%Y-%m-%d'
            if "-" in txt:
                fmt = '%Y-%m-%d'
            elif "/" in txt:
                fmt = '%Y/%m/%d'
            return datetime.datetime.strptime(txt, fmt)
        else:
            raise TypeError

    def datetime_to_timestamp(self, datetime):
        return int(datetime.timestamp())

    def datetime_now(self):
        return datetime.datetime.now()

    def safe_remove_key_from_dict(self, my_dict, my_key):
        try:
            del my_dict[my_key]
            return True
        finally:
            return False

    def timestamp_to_datetime_as_dict(self, timestamp):
        lt = time.localtime(timestamp)
        data_set = {
            'year': time.strftime('%Y', lt),
            'month': time.strftime('%m', lt),
            'day': time.strftime('%d', lt),
            'hour': time.strftime('%H', lt),
            'minute': time.strftime('%M', lt),
            'second': time.strftime('%S', lt),
        }
        return data_set

    def timestamp_curr_time(self):
        return int(time.time())

    def time_diff(self, datetime_a, datetime_b):
        time_diff_d = datetime_a - datetime_b
        time_diff_r1 = str(time_diff_d).split(', ')
        if len(time_diff_r1) > 1:
            time_diff_r1 = time_diff_r1[1]
            time_diff_r2 = time_diff_r1.split(':')
        else:
            time_diff_r2 = time_diff_r1[0].split(':')
        time_diff_day = str(time_diff_d.days).split(' day')
        time_diff_day = int(float(time_diff_day[0]))
        day2hour = time_diff_day * 24

        dt_set = {
            'day': time_diff_day,
            'hour': int(float(time_diff_r2[0])) + day2hour,
            'minute': int(float(time_diff_r2[1])),
            'second': int(float(time_diff_r2[2])),
        }
        return dt_set

    def dict_to_object(self, dict_obj):
        if not isinstance(dict_obj, dict):
            return dict_obj
        inst = Dict()
        for k, v in dict_obj.items():
            inst[k] = self.dict_to_object(v)
        return inst
