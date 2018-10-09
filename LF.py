import requests,os,time,csv,sqlite3,subprocess,configparser,pymysql,xlrd,codecs
import urllib.parse as parse
from xlutils.copy import copy
from functools import reduce
from xlwt import Style
import win32com.client
import pythoncom

class ErrMsg():

    UnsupportStr = "不支持输入字符"
    UnableAccessThisFile = "另一个程序正在使用此文件，进程无法访问。"
    def __init__(self,UnsupportStr,UnableAccessThisFile):
        self.UnsupportStr = UnsupportStr
        self.UnableAccessThisFile = UnableAccessThisFile

class Msg():
    StartGetToken = "开始获取Token"
    GetTokenSuccess = "获取Token成功"
    StartGetData = "开始获取数据"
    GetDataSuccess = "获取数据成功"
    StartWriteData = "开始写入数据"
    WriteDataSuccess = "写入数据成功!"
    NoNetWorkConnection = "没有网络连接,请重试"
    ContinueOrQuit = "按任意键继续或按Q退出"
    UnsupportedDB = "不支持此类型数据库"
    WrongDataFormat = "API返回的数据格式错误,请重试"
    UnknowProfileID = "未知的配置项,请重试."
    SelectProfile = "请选择一项配置进行数据下载与分析"
    SelectProfileUpline = "=[ID]=[Profile]==========="
    SelectProfileDownline = "=========================="
    CopyFileToRawData = "复制文件到RawData文件夹"
    CallMergeBat = "调用Merge.bat"
    CopyFileToData = "复制文件到Data文件夹"
    CallStartBat = "调用Start.bat"
    OpenDataFolder = "打开Data文件夹"
    FailedGetAccentToken = "获取AccentToken失败请重试"
    ContinueOrQuitForRetryFunction = "已尝试10次,是否需要继续重试10次?"
    TimeCountOfRetry = "正在重试第<<%s>>次"
    UnknowSelection = "UnknowSelection"

    def __init__(self, StartGetToken, GetTokenSuccess, StartGetData, StartWriteData,
                 WriteDataSuccess, NoNetWorkConnection, WrongDataFormat, UnknowProfileID,
                 SelectProfile, SelectProfileUpline, SelectProfileDownline, CopyFileToRawData,
                 CallMergeBat, CopyFileToData, CallStartBat, OpenDataFolder, FailedGetAccentToken, UnknowSelection):
        self.StartGetToken = StartGetToken
        self.FinishGetToken = GetTokenSuccess
        self.StartGetData = StartGetData
        self.StartWriteData = StartWriteData
        self.WriteSuccess = WriteDataSuccess
        self.NoNetWorkConnection = NoNetWorkConnection
        self.WrongDataFormat = WrongDataFormat
        self.UnknowProfileID = UnknowProfileID
        self.SelectProfile = SelectProfile
        self.SelectProfileUpline = SelectProfileUpline
        self.SelectProfileDownline = SelectProfileDownline
        self.CopyFileToRawData = CopyFileToRawData
        self.CallMergeBat = CallMergeBat
        self.CopyFileToData = CopyFileToData
        self.CallStartBat = CallStartBat
        self.OpenDataFolder = OpenDataFolder
        self.FailedGetAccentToken = FailedGetAccentToken
        self.UnknowSelection = UnknowSelection

class Infra():

    def OpenDir(self,Dir):
        os.system("explorer %s" % DaPr.ReplaceDirSlash(self,Dir))

    def OpenFile(self, Program,Dir,Param):
        if Param == None:
            ParamX = ' '
        else:
            ParamX = Param
        os.system("%s %s %s" % (Program,DaPr.ReplaceDirSlash(self, Dir),ParamX))

    def PostWR(self, DataSource, Parameter):
        Counter = 0
        Response = Infra.Post(self, DataSource, Parameter)
        while Response == False:
            time.sleep(1)
            if Counter == 10:
                if input("已经尝试10次是否继续?(y/n)") in ['y', 'Y']:
                    Counter = 0
                    Response = Infra.Post(self, DataSource, Parameter)
                else:
                    break
            else:
                Response = Infra.Post(self, DataSource, Parameter)
                Counter += 1
        else:
            return Response

    def GetWR(self, DataSource, Parameter):
        Counter = 0
        Response = Infra.Get(self, DataSource, Parameter)
        while Response == False:
            time.sleep(1)
            if Counter == 10:
                if input("已经尝试10次是否继续?(y/n)") in ['y', 'Y']:
                    Counter = 0
                    Response = Infra.Get(self, DataSource, Parameter)
                else:
                    break
            else:
                Response = Infra.Get(self, DataSource, Parameter)
                Counter += 1
        else:
            return Response

    def Post(self, DataSource, Parameter):
        try:
            # 构造并发送Post请求
            Request = requests.post(DataSource, Parameter)
            # 定义返回数据变量名称
            Response = Request.json()
            # 返回响应报文
            return Response
        except:
            # 输出"无网络连接"消息
            print(Msg.NoNetWorkConnection)
            time.sleep(5)
            # 返回 Main.Flow(sel返回到方法
            return False

    def Get(self, DataSource, ParameterDict):
        try:
            # 构造并发送Get请求(在APIUrl后加入查询参数的字典)
            Request = "%s?%s" % (DataSource, parse.urlencode(ParameterDict))
            # Request = RawRequest.encode("utf-8")
            # print(Request)
            # 定义返回报文变量名称
            Response = requests.get(Request)
            return Response
        except:
            # 输出"无网络连接"消息
            print(Msg.NoNetWorkConnection)
            # time.sleep(5)
            # 返回 Main.Flow(sel返回到方法
            return False

    def MariaDB(SQL, Host, Port, User, Password, Database, CharSet, Data, NumberOfRow, ):
        try:
            # 连接MySQL数据库
            ConnectDataBase = pymysql.connect(host=Host, port=Port, user=User, password=Password, db=Database,
                                              charset=CharSet,cursorclass=pymysql.cursors.DictCursor)
            # 通过cursor创建游标
            DataBaseCursor = ConnectDataBase.cursor()
            # 执行数据查询
            DataBaseCursor.execute(SQL)
            if Data == "None":
                DataBaseCursor.execute(SQL)
                if NumberOfRow == 1:
                    RawData = DataBaseCursor.fetchone()
                    ConnectDataBase.Close()
                    return RawData
                if NumberOfRow > 0:
                    RawData = DataBaseCursor.fetchmany(NumberOfRow)
                    ConnectDataBase.Close()
                    return RawData
                else:
                    RawData = DataBaseCursor.fetchall()
                    ConnectDataBase.Close()
                    return RawData
            else:
                DataBaseCursor.execute(SQL)
                ConnectDataBase.commit()
                ConnectDataBase.Close()
                return True
        except:
            return False

    def SQLite3(SQL, Data, OutputType, NumberOfRow, Database):

        try:
            if OutputType != 'Dict':
                ConnectDataBase = sqlite3.connect(Database)
                CursorDataBase = ConnectDataBase.cursor()
                ConnectDataBase.row_factory = Infra.dict_factory
            else:
                ConnectDataBase = sqlite3.connect(Database)
                CursorDataBase = ConnectDataBase.cursor()

            if Data == None:
                SQLS = CursorDataBase.execute(SQL)
                if NumberOfRow == 1:
                    RawData = SQLS.fetchone()
                elif NumberOfRow > 0:
                    RawData = SQLS.fetchmany(NumberOfRow)
                else:
                    RawData = SQLS.fetchall()
                if OutputType == "List":
                    return DaPr.MergeMultiTupleList(object,RawData)
                else:
                    return RawData
            else:
                CursorDataBase.execute(SQL, Data)
                ConnectDataBase.commit()
        except:
            # print("[!!]数据库写入失败请联系yzxia@hitachi-systems.cn")
            return False

    def SQLite3Debug(SQL, Data, OutPutType, NumberOfRow, Database):
        ConnectDataBase = sqlite3.connect(Database)
        CursorDataBase = ConnectDataBase.cursor()

        if Data == None:
            SQLS = CursorDataBase.execute(SQL)
            if NumberOfRow == 1:
                RawData = SQLS.fetchone()
            elif NumberOfRow > 0:
                RawData = SQLS.fetchmany(NumberOfRow)
            else:
                RawData = SQLS.fetchall()
            if OutPutType == "List":
                return DaPr.MergeMultiTupleList(RawData)
            else:
                return RawData
        else:
            CursorDataBase.execute(SQL, Data)
            ConnectDataBase.commit()

    def ExcuteBat(self, BatFilePath,BatFile):
        BatFilePath = ("%s\\%s" % (BatFilePath, BatFile))
        ExcuetBat = subprocess.Popen("cmd.exe /c" + "%s abc" % BatFilePath, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        Curline = ExcuetBat.stdout.readline()
        while (Curline != b''):
            # print(Curline.decode('GBK'))
            Curline = ExcuetBat.stdout.readline()
        ExcuetBat.wait()
        # print(ExcuteBat.returncode)
        ExcuetBat.terminate()

    def Readini(ConfigFile,Section,Key):
        ReadConfig = configparser.ConfigParser()
        ReadConfig.read_file(codecs.open(ConfigFile, "r", "utf-8-sig"))
        # ReadConfig.sections()
        ReadConfig.options(Section)
        # ReadConfig.items(Section)
        Value = ReadConfig.get(Section, Key)
        return Value

    def ReadiniAsDict(ConfigFile):
        ReadConfig = configparser.ConfigParser()
        ReadConfig.read_file(codecs.open(ConfigFile, "r", "utf-8-sig"))
        Dict = dict(ReadConfig._sections)
        for Key in Dict:
            Dict[Key] = dict(Dict[Key])
        return Dict

    def AdoDBCon(self, Mode, Host, DB, User, Passsowrd, Proxy, ProxyPort, SQL,Outputtype):
        ConnParm = {'host': r"%s"%Host,
                     'database': DB,
                     'user': User,
                     'password': Passsowrd}
        ConnParm['connection_string'] = """Provider=SQLOLEDB.1;
        User ID=%(user)s; Password=%(password)s;
        Initial Catalog=%(database)s; Data Source= %(host)s"""
        if len(Proxy) > 1:
            import adodbapi.remote as AdoLib
            ConnParm['proxy_host'] = Proxy
            if len(ProxyPort) > 1:
                ConnParm['proxy_port'] = ProxyPort
            else:pass
        else:
            import adodbapi as AdoLib
        Ado = AdoLib.connect(ConnParm)
        AdoCur = Ado.cursor()
        if Mode == 'w':
            try:
                AdoCur.execute(SQL)
                Ado.commit()
                Ado.close()
                return True
            except Exception as err:
                print(err)
                return False
        else:
            if Outputtype == 'Dict':
                AdoCur.execute(SQL)
                Columns = [column[0] for column in AdoCur.description]
                RawData = []
                for Row in AdoCur.fetchall():
                    RawData.append(dict(zip(Columns, Row)))
                Ado.close()
                return RawData
            else:
                AdoCur.execute(SQL)
                RawData = []
                for Row in AdoCur.fetchall():
                    for Rowdata in Row:
                        RawData.append(Rowdata)
                Ado.close()
                return RawData

class SaveData():

    def toCSV(self, FilePath, FileName, Headers, Data):
        LogPath = ("%s%s" % (FilePath, FileName))
        print(Msg.StartWriteData)
        with open(LogPath, 'w',newline='') as CSV:
            # 定义Writer对象(由CSV.DictWriter(以字典模式写入)模块组成并定义列名称)
            Writer = csv.DictWriter(CSV, fieldnames=Headers)
            # 写入列名称(字典的键)
            Writer.writeheader()
            # 循环写入列表中每一条数据到CSV文件
            for Row in Data:
                # 写入元素(字典的值)
                Writer.writerow(Row)
        print(Msg.WriteDataSuccess)
        CSV.close()

    def toCSVSR(self,CSV,Headers, Data):
        # 定义Writer对象(由CSV.DictWriter(以字典模式写入)模块组成并定义列名称)
        Writer = csv.DictWriter(CSV, fieldnames=Headers)
        # 写入列名称(字典的键)
        Writer.writeheader()
        # 写入元素(字典的值)
        Writer.writerow(Data)
        # print(Msg.WriteDataSuccess)
        CSV.Close()

    def toTXT(self, FilePath, FileName, Data):
        # 定义文件路径
        LogPath = ("%s\%s" % (FilePath, FileName))
        # 打开文件
        with open(LogPath, 'w', encoding='utf-8') as Log:
            # 写入数据
            Log.write(Data)
            # 输出"写入数据成功数据"
            print(Msg.WriteDataSuccess)
            # 打开数据存储文件夹
            os.system("explorer.exe %s\Logs" % FilePath)
        return LogPath

    def toXls(self, File, Row, Col, Str, Style=Style.default_style):
        # 合并单元格:
        # ws.write_merge(top_row, bottom_row, left_column, right_column, string)
        rb = xlrd.open_workbook(File, formatting_info=True)
        wb = copy(rb)
        ws = wb.get_sheet(0)
        ws.write(Row, Col, Str, Style)
        wb.Save(File)

    def ModifyExcel(self,FilePath,Filename,RowColSet,Data):
        book = xlrd.open_workbook(Filename)  # 打开excel
        new_book = copy(book)  # 复制excel
        sheet = new_book.get_sheet(0)  # 获取第一个表格的数据
        for RowCol in RowColSet:
            sheet.write(RowCol[0], RowCol[1], Data)  # 修改0行1列的数据为'Haha'
        TempFile = FilePath + '\Temp.xls'
        new_book.Save(TempFile)  # 保存新的excel
        try:
            os.remove(Filename)  # 删除旧的excel
            os.rename(TempFile, Filename)  # 将新excel重命名
        except:print(ErrMsg.UnableAccessThisFile)

class FormatCurrentTime():
    YYYYMMDDHHMMSS = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    YYYYMMDD = time.strftime("%Y%m%d", time.localtime())
    def __init__(self,YYYYMMDDHHMMSS,YYYYMMDD):
        self.YYYYMMDDHHMMSS = YYYYMMDDHHMMSS
        self.YYYYMMDD = YYYYMMDD

class Numbers():

    def GenRange(self, StartNumber, EndNumber, GapNumber):
        NumberRangeResult = []
        RowNumberSP = StartNumber
        Gap = int(EndNumber) - int(StartNumber)
        if Gap > GapNumber:
            for X in range(int(Gap / GapNumber)):
                Temp = []
                Temp.append(RowNumberSP)
                Temp.append(RowNumberSP + GapNumber)
                NumberRangeResult.append(Temp)
                RowNumberSP += GapNumber
            Temp = []
            Temp.append(RowNumberSP)
            Temp.append(RowNumberSP + int(Gap % GapNumber))
            NumberRangeResult.append(Temp)
            RowNumberSP += int(Gap % GapNumber)
        else:
            NumberRangeResult.append([StartNumber,EndNumber])
        return NumberRangeResult

class DaPr():

    def SQLMakerForMSSQL(self,OprType,Config):
        '''
        Config Template
           Config = {
           'Database':'TMS_ATL',
           'DBO':'dbo',
           'TableName':'M-Delivery',
           'WhereArgs':'[Name] IS NOT NULL',
           'NumberOfRow':1000,
           'Cols':[1,2,3],
           'Values':[1,2,3],
           }
        '''
        Unziped = {
            'Temp':[],
            'Cols':None,
            'Values':None,
            'WhereIsNotNull':None,
        }
        GUA = ['Cols','WhereIsNotNull']#The gourp is using '[]'
        GUB = ['Values']#The gourp is using ''''
        for DataSet in GUA + GUB:
            if len(Config[DataSet]) > 0:
                for Element in Config[DataSet]:
                    if DataSet in GUA:
                        Unziped['Temp'].append("[%s]"%Element)
                    elif DataSet in GUB:
                        Unziped['Temp'].append("'%s'" % Element)
                Unziped[DataSet] = reduce(lambda x, y: x + y, DaPr.InsertIntoValuesToList(self, Unziped['Temp'], ","))
                Unziped['Temp'].clear()
            else:pass
        SQLTemplats = {
            'SelectRaw': "SELECT %s FROM [%s].[%s].[%s] " % (Config['SelectType'], Config['Database'], Config['DBO'], Config['TableName']),
            'Select': "SELECT %s FROM [%s].[%s].[%s] WHERE %s IS NOT NULL " % (Config['SelectType'],Config['Database'], Config['DBO'], Config['TableName'], Unziped['WhereIsNotNull']),
            'Insert':"INSERT INTO [%s].[%s].[%s](%s) VALUES(%s)" % (Config['Database'],Config['DBO'],Config['TableName'],Unziped['Cols'],Unziped['Values']),
            'Update':"UPDATE [%s].[%s].[%s] SET Address = 'Zhongshan 23', City = 'Nanjing' WHERE LastName = 'Wilson'"%(Config['Database'], Config['DBO'], Config['TableName'],)
        }
        return SQLTemplats[OprType]

    def KeepOne(self,rawdata):
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
                    FilePath = Files[0] + '\\' + FileName
                    FileList.append((FileName, os.path.getctime(FilePath),FilePath))
        if len(FileList) > 1:
            return sorted(FileList, key=lambda FileCreateTime: FileCreateTime[1])[-1][2]
        else:
            return False

    def ReplaceDirSlash(self,Dir):
        return reduce(lambda x, y: x + y, DaPr.InsertIntoValuesToList(self, Dir.split("/"), "\\"))

    def RenameDictKeys(self,RawData,ReplaceKeyMap):
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

    def MergeMultiTupleList(self,TupleList):
        List = []
        for Tuple in TupleList:
            for Data in Tuple:
                List.append(Data)
        return List

    def MergeTwoDicts(self,DictA,DicB):
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

    def RootPath(self,RootDirName):
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
        return reduce(lambda x, y: x + y, DaPr.InsertIntoValuesToList(self, Temp, '\\'))

    def ConvertTwoListsToDict(self, ListForKey, ListForValue):
        Dict = dict(zip(ListForKey,ListForValue))
        return Dict

    def Dedupe(self,DataSet):
        Package = []
        for Data in  DataSet:
            if Data not in Package:
                Package.append(Data)
            else:pass
        return Package

class Exl():

    def GetColDataByHeader(self, excel, sheetName, head):
        import math,pandas
        # print(pandas.read_excel(excel,sheet_name='T-Commbox',index_col='CityCode'))
        ExcelFile = pandas.read_excel(excel, sheet_name=sheetName)
        Bucket = []
        # print(xl.to_dict())
        # print(xl.values.tolist())
        Headers = []
        for Head in ExcelFile.keys():
            Headers.append(Head)
        for Data in ExcelFile.get_values():
            print(Data)
            data = Data[Headers.index(head)]
            try:
                math.isnan(data)
                pass
            except:
                Bucket.append(data)
        return Bucket

    def GetColDataByHeaderWithCOM(self, excel, sheetName, head,Range,DoNotShowNone):
        ExlFile = ExlCom(filename=excel, isReadOnly=False, isVisible=False)
        Datasource = ExlFile.GetRange(sheet=sheetName, col1=Range[0], row1=Range[1], col2=Range[2], row2=Range[3])
        # print(Datasource)
        HeaderNum = None
        DataSet = []
        for EachRowOfData in Datasource:
            # print(EachRowOfData)
            if HeaderNum == None:
                EachRowOfDataList = []
                for Element in EachRowOfData:
                    # print(Element)
                    EachRowOfDataList.append(Element)
                if head in EachRowOfDataList:
                    HeaderNum = EachRowOfDataList.index(head)
            else:
                if DoNotShowNone == True:
                    if EachRowOfData[HeaderNum] == None:
                        pass
                    else:
                        DataSet.append(EachRowOfData[HeaderNum])
                else:
                    DataSet.append(EachRowOfData[HeaderNum])
        ExlFile.Close(0)
        return DataSet

    def WriteDataToExcel(self, excel, sheetName,Dataset):
        from openpyxl import load_workbook
        Workbook = load_workbook(excel,read_only=False, keep_vba=True)
        SelectedSheet = Workbook[sheetName]
        for data in Dataset:
            SelectedSheet[data['Cell']] = data['Data']
        Workbook.save(excel)

    def VBACon(self, VBAFile, VBAFunction,ExcelVisible,SaveChanges,ResultPath, ResultFileType):
        print("CreatExcelApp")
        ExcelBook = ExlCom(VBAFile,isVisible=ExcelVisible)
        print("ExecuVBAFunction")
        ExcelBook.RunVBA(VBAFunction)
        print("CloseExcelFile")
        ExcelBook.Close(SaveChanges=SaveChanges)  # 关闭excel，不保存
        if ResultPath == None:pass
        else:
            print("OpenResult")
            Infra.OpenFile(self,'start', DaPr.FindNewestFileInWindows(self, ResultPath, ResultFileType), None)
        print("JobDone")

class ExlCom:
        """A utility to make it easier to get at Excel.    Remembering
        to Save the data is your problem, as is    error handling.
        Operates on one workbook at a time."""

        def __init__(self, filename=None, isVisible=None, isReadOnly=None, Format=None, Password=None,
                     WriteResPassword=None):  # 打开文件或者新建文件（如果不存在的话）
            pythoncom.CoInitialize()
            self.xlApp = win32com.client.Dispatch('Excel.Application')
            self.xlApp.Visible = isVisible
            if filename:
                self.filename = filename
                self.xlBook = self.xlApp.Workbooks.Open(filename, ReadOnly=isReadOnly, Format=Format, Password=Password,
                                                        WriteResPassword=WriteResPassword)
            else:
                self.xlBook = self.xlApp.Workbooks.Add()
                self.filename = ''

        def RunVBA(self,VBAFunction):
            strPara = self.xlBook.Name + VBAFunction
            status = self.xlApp.ExecuteExcel4Macro(strPara)
            # print(status)

        def Save(self, newfilename=None):  # 保存文件
            if newfilename:
                self.filename = newfilename
                self.xlBook.SaveAs(newfilename)
            else:
                self.xlBook.Save()

        def Close(self,SaveChanges):  # 关闭文件
            self.xlBook.Close(SaveChanges=SaveChanges)
            del self.xlApp
            # pythoncom.CoUninitialize()

        def GetCell(self, sheet, row, col):  # 获取单元格的数据
            "Get value of one cell"
            sht = self.xlBook.Worksheets(sheet)
            return sht.Cells(row, col).Value

        def SetCell(self, sheet, row, col, value):  # 设置单元格的数据
            "set value of one cell"
            Sheet = self.xlBook.Worksheets(sheet)
            Sheet.Cells(row, col).Value = value

        def SetCellFormat(self, sheet, row, col):  # 设置单元格的数据
            "set value of one cell"
            Sheet = self.xlBook.Worksheets(sheet)
            Sheet.Cells(row, col).Font.Size = 15  # 字体大小
            Sheet.Cells(row, col).Font.Bold = True  # 是否黑体
            Sheet.Cells(row, col).Name = "Arial"  # 字体类型
            Sheet.Cells(row, col).Interior.ColorIndex = 3  # 表格背景
            # sht.Range("A1").Borders.LineStyle = xlDouble
            Sheet.Cells(row, col).BorderAround(1, 4)  # 表格边框
            Sheet.Rows(3).RowHeight = 30  # 行高
            Sheet.Cells(row, col).HorizontalAlignment = -4131  # 水平居中xlCenter
            Sheet.Cells(row, col).VerticalAlignment = -4160  #

        def DeleteRow(self, sheet, row):
            sht = self.xlBook.Worksheets(sheet)
            sht.Rows(row).Delete()  # 删除行
            sht.Columns(row).Delete()  # 删除列

        def GetRange(self, sheet, row1, col1, row2, col2):  # 获得一块区域的数据，返回为一个二维元组
            "return a 2d array (i.e. tuple of tuples)"
            sht = self.xlBook.Worksheets(sheet)
            return sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value

        def AddPicture(self, sheet, pictureName, Left, Top, Width, Height):  # 插入图片
            "Insert a picture in sheet"
            sht = self.xlBook.Worksheets(sheet)
            sht.Shapes.AddPicture(pictureName, 1, 1, Left, Top, Width, Height)

        def CopySheet(self, before):  # 复制工作表
            "copy sheet"
            shts = self.xlBook.Worksheets
            shts(1).Copy(None, shts(1))

        def InserRow(self, sheet, row):
            sht = self.xlBook.Worksheets(sheet)
            sht.Rows(row).Insert(1)

# Host = '.\SQLEXPRESS'
# DB = 'TMS_ATL'
# User = 'python'
# Passsowrd = '262122'
# Proxy =  ''
# PoxyPort = ''
#
# Config = {
#     'Database':'TMS_ATL',
#     'DBO':'dbo',
#     'TableName':'InitialSetting',
#     'WhereArgs':'[Name] IS NOT NULL',
#     'NumberOfRow':1000,
#     'Cols':[1,2,3],
#     'Values':[1,2,3],
# }
# print(Infra.AdoDBCon(object, 'r', Host, DB, User, Passsowrd, Proxy, PoxyPort, DaPr.SQLMakerForMSSQL(object,'SelectAll',Config),'List'))



# for x in range(100):
#     SQL = "INSERT INTO [HCHSPB].[dbo].[TestTable]([TestABC],[TGHHA]) VALUES('%s','%s')" % ('python %s'%x,'python%s'%x)
#     print(Infra.AdoDBCon(object, 'w', Host, DB, User, Passsowrd, Proxy, PoxyPort, SQL))

