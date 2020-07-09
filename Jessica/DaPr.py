import datetime
import os
import re
import time
from functools import reduce

import prettytable


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


class Core(object):

    @staticmethod
    def show_selection_table(selection_list, table_head, question_text):
        pt = prettytable.PrettyTable()
        pt.field_names = table_head
        for i in range(len(selection_list)):
            row_id = i
            row = selection_list[i]
            row.insert(0, row_id)
            pt.add_row(row)
        print(pt)
        selected = input(question_text)
        return selection_list[int(selected)]

    @staticmethod
    def del_invalid_str(regx, o_str):
        result = re.sub(regx, '', o_str)
        return result

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

    @staticmethod
    def tuple_list_to_list(tuple_list):
        list_i = []
        for tuple_i in tuple_list:
            list_i.append(tuple_i[0])
        return list_i

    @staticmethod
    def find_diff_value_from_two_dicts(type_i, origi, modified):
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
                    file_path = os.path.join(Files[0], FileName)
                    file_list.append((FileName, os.path.getctime(file_path), file_path))
        if len(file_list) > 1:
            return sorted(file_list, key=lambda file_create_time: file_create_time[1])[-1][2]
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

    @staticmethod
    def clean_list(str_i, split_str, *args):
        raw = str_i.split(split_str)
        new = []
        for x in raw:
            if x not in args:
                new.append(x)
        return new

    @staticmethod
    def gen_path(drive, list_s):
        drive_l = [drive]
        list_n = drive_l + list_s
        path = os.path.join(*list_n)
        return path

    def insert_value_to_list_and_merge(self, u_list, value):
        if type(u_list) is not list:
            return u_list
        tmp = self.insert_values_to_list(u_list, value)
        if len(tmp) > 0:
            return reduce(lambda x, y: x + y, tmp)
        else:
            return ""

    @staticmethod
    def list_to_string(u_list):
        return reduce(lambda x, y: x + y, u_list)

    @staticmethod
    def rename_dict_keys(raw_data, replace_key_map):
        for Key in raw_data:
            for rd_key, rd_value in replace_key_map.items():
                if Key == rd_key:
                    raw_data[rd_value] = raw_data.pop(Key)
        return raw_data

    @staticmethod
    def insert_values_to_list(data_set, insert_value):
        union_data = []
        if isinstance(data_set, list):
            for Data in data_set:
                union_data.append(Data)
                union_data.append(insert_value)
            if len(union_data) > 0:
                del union_data[-1]
            else:
                pass
            return union_data
        else:
            return data_set

    @staticmethod
    def insert_into_x_values_to_list(data_set, gap, insert_value):
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

    @staticmethod
    def unpack_list_and_insert_values_to_list(data_set, insert_value):
        union_data = []
        for List in data_set:
            for Data in List:
                union_data.append(Data)
            union_data.append(insert_value)
        del union_data[-1]
        return union_data

    @staticmethod
    def merge_multi_tuple_list(tuple_list):
        raw_list = []
        for Tuple in tuple_list:
            for Data in Tuple:
                raw_list.append(Data)
        return raw_list

    @staticmethod
    def merge_lists(data_list, *args):
        base = ["place_holder"]
        for data in data_list:
            base.extend(data)
        if len(args) != 0:
            for list_data in args:
                for list_item in list_data:
                    base.extend(list_item)
        base.pop(0)
        return base

    @staticmethod
    def merge_two_dicts(dict_a, dic_b):
        merged_dict = {}
        for Key, Value in dict_a.items():
            merged_dict[Key] = Value
        for Key, Value in dic_b.items():
            merged_dict[Key] = Value
        return merged_dict

    @staticmethod
    def find_valid_data_from_dict(valid_data_name, dict_i):
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

    @staticmethod
    def convert_two_lists_to_dict(list_for_key, list_for_value):
        new_dict = dict(zip(list_for_key, list_for_value))
        return new_dict

    @staticmethod
    def dedupe(dataset):
        package = []
        for Data in dataset:
            if Data not in package:
                package.append(Data)
            else:
                pass
        return package

    @staticmethod
    def timestamp_to_datetime(timestamp):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))

    @staticmethod
    def string_to_datetime(txt):
        if type(txt) is str:
            fmt = '%Y-%m-%d'
            if "-" in txt:
                fmt = '%Y-%m-%d'
            elif "/" in txt:
                fmt = '%Y/%m/%d'
            return datetime.datetime.strptime(txt, fmt)
        else:
            raise TypeError

    @staticmethod
    def datetime_to_timestamp(date_time):
        return int(date_time.timestamp())

    @staticmethod
    def datetime_now():
        return datetime.datetime.now()

    @staticmethod
    def safe_remove_key_from_dict(my_dict, my_key):
        try:
            del my_dict[my_key]
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def timestamp_to_datetime_as_dict(timestamp):
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

    @staticmethod
    def timestamp_curr_time():
        return int(time.time())

    @staticmethod
    def time_diff(datetime_a, datetime_b):
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

    def convert_multiline_to_single_line(self, data, connect_str, *args):
        return self.insert_value_to_list_and_merge(self.clean_list(data, "\n", *args), connect_str)
