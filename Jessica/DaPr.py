from lfcomlib.Jessica import os, time, datetime, reduce


class DaPr:

    def FindDiffValueFromTwoDicts(self, type, Origi, Modified):
        if type in ['dict', 'Dict']:
            Diff = {}
            for Key, Value in Origi.items():
                try:
                    if Modified[Key] == Value:
                        pass
                    else:
                        Diff[Key] = Value
                except:
                    pass
            return Diff

    def KeepOne(self, rawdata):
        KeepOne = []
        Package = []
        for Data in rawdata:
            if Data not in KeepOne:
                KeepOne.append(Data)
                Package.append({'value': Data, 'label': Data})
            else:
                pass
        KeepOne.clear()
        print(Package)
        return Package

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

    def ConvertTwoListsToDict(self, ListForKey, ListForValue):
        Dict = dict(zip(ListForKey, ListForValue))
        return Dict

    def Dedupe(self, DataSet):
        Package = []
        for Data in DataSet:
            if Data not in Package:
                Package.append(Data)
            else:
                pass
        return Package

    def TimestampToDateTime(self, timestamp):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))

    def DatetimeToTimestamp(self, datetime):
        return int(datetime.timestamp())

    def DatetimeNow(self):
        return datetime.datetime.now()

    def TimestampToDateTimeAsDict(self, timestamp):
        lt = time.localtime(timestamp)
        dtset = {
            'year': time.strftime('%Y', lt),
            'month': time.strftime('%m', lt),
            'day': time.strftime('%d', lt),
            'hour': time.strftime('%H', lt),
            'minite': time.strftime('%M', lt),
            'second': time.strftime('%S', lt),
        }
        return dtset

    def TimestampCurrTime(self):
        return int(time.time())

    def TimeDiff(self, datetimeA, datetimeB):
        timediff = datetimeA - datetimeB
        timediffR1 = str(timediff).split(', ')
        if len(timediffR1) > 1:
            timediffR1 = timediffR1[1]
            timediffR2 = timediffR1.split(':')
        else:
            timediffR2 = timediffR1[0].split(':')
        timediffDay = str(timediff.days).split(' day')
        timediffDay = int(float(timediffDay[0]))
        day2hour = timediffDay * 24

        dtset = {
            'day': timediffDay,
            'hour': int(float(timediffR2[0])) + day2hour,
            'minute': int(float(timediffR2[1])),
            'second': int(float(timediffR2[2])),
        }
        return dtset
