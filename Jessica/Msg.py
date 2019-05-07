class Msg:
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