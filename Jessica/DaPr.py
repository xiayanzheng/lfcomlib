from lfcomlib.Jessica import os, time, datetime, reduce


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


class DaPr:

    def find_diff_value_from_two_dicts(self, type, Origi, Modified):
        if type in ['dict', 'Dict']:
            diff = {}
            for Key, Value in Origi.items():
                try:
                    if Modified[Key] == Value:
                        pass
                    else:
                        diff[Key] = Value
                except:
                    pass
            return diff

    def keep_one(self, rawdata):
        keep_one = []
        package = []
        for Data in rawdata:
            if Data not in keep_one:
                keep_one.append(Data)
                package.append({'value': Data, 'label': Data})
            else:
                pass
        keep_one.clear()
        return package

    def FindNewestFileInWindows(self, Dir, FileExtensionList):
        FileList = []
        for Files in os.walk(Dir):
            for FileName in Files[2]:
                if FileName.split(".")[-1] in FileExtensionList:
                    FilePath = os.path.join(Files[0], FileName)
                    FileList.append((FileName, os.path.getctime(FilePath), FilePath))
        if len(FileList) > 1:
            return sorted(FileList, key=lambda FileCreateTime: FileCreateTime[1])[-1][2]
        else:
            return False

    def ReplaceDirSlash(self, Dir):
        return reduce(lambda x, y: x + y, self.InsertIntoValuesToList(Dir.split("/"), "\\"))

    def ReplaceDirSymbol(self, Dir, ReplaceFrom, ReplaceTo):
        return reduce(lambda x, y: x + y, self.InsertIntoValuesToList(Dir.split(ReplaceFrom), ReplaceTo))

    def RenameDictKeys(self, RawData, ReplaceKeyMap):
        for Key in RawData:
            for RDKey, RDVaule in ReplaceKeyMap.items():
                if Key == RDKey:
                    RawData[RDVaule] = RawData.pop(Key)
        return RawData

    def InsertIntoValuesToList(self, DataSet, InsertValue):
        UnionData = []
        for Data in DataSet:
            UnionData.append(Data)
            UnionData.append(InsertValue)
        del UnionData[-1]
        return UnionData

    def InsertIntoXValuesToList(self, DataSet, Gap, InsertValue):
        UnionData = []
        Count = 0
        if len(DataSet) > Gap:
            for Data in DataSet:
                if Count < Gap:
                    UnionData.append(Data)
                    Count += 1
                else:
                    UnionData.append(InsertValue)
                    Count = 0
            del UnionData[-1]
        else:
            for Data in DataSet:
                UnionData.append(Data)
        return UnionData

    def UnpackageListAndInsertValuesToList(self, DataSet, InsertValue):
        UnionData = []
        for List in DataSet:
            for Data in List:
                UnionData.append(Data)
            UnionData.append(InsertValue)
        del UnionData[-1]
        return UnionData

    def MergeMultiTupleList(self, TupleList):
        List = []
        for Tuple in TupleList:
            for Data in Tuple:
                List.append(Data)
        return List

    def MergeTwoDicts(self, DictA, DicB):
        MergedDict = {}
        for Key, Value in DictA.items():
            MergedDict[Key] = Value
        for Key, Value in DicB.items():
            MergedDict[Key] = Value
        return MergedDict

    def FindValidDataFromDict(self, ValidDataName, Dict):
        ValidData = {}
        for Key, Value in Dict.items():
            if Key in ValidDataName:
                ValidData[Key] = Value
        return ValidData

    def RootPath(self, RootDirName):
        try:
            initPath = os.getcwd().split('\\')
        except:
            initPath = os.getcwd().split('/')
        Temp = []
        for Folder in initPath:
            if Folder != RootDirName:
                Temp.append(Folder)
            else:
                Temp.append(RootDirName)
                break
        return reduce(lambda x, y: x + y, self.InsertIntoValuesToList(Temp, '\\'))

    def convert_two_lists_to_dict(self, ListForKey, ListForValue):
        dict = dict(zip(ListForKey, ListForValue))
        return dict

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
            'minite': time.strftime('%M', lt),
            'second': time.strftime('%S', lt),
        }
        return data_set

    def timestamp_curr_time(self):
        return int(time.time())

    def time_diff(self, datetimeA, datetimeB):
        time_diff = datetimeA - datetimeB
        time_diff_r1 = str(time_diff).split(', ')
        if len(time_diff_r1) > 1:
            time_diff_r1 = time_diff_r1[1]
            time_diff_r2 = time_diff_r1.split(':')
        else:
            time_diff_r2 = time_diff_r1[0].split(':')
        time_diff_day = str(time_diff.days).split(' day')
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
