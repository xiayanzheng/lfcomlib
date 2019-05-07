from lfcomlib.Jessica import Infra, DaPr


class Exl:

    def GetColDataByHeader(self, excel, sheetName, head):
        import math, pandas
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

    def GetColDataByHeaderWithCOM(self, excel, sheetName, head, Range, DoNotShowNone):
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

    def WriteDataToExcel(self, excel, sheetName, Dataset):
        from openpyxl import load_workbook
        Workbook = load_workbook(excel, read_only=False, keep_vba=True)
        SelectedSheet = Workbook[sheetName]
        for data in Dataset:
            SelectedSheet[data['Cell']] = data['Data']
        Workbook.save(excel)

    def VBACon(self, VBAFile, VBAFunction, ExcelVisible, SaveChanges, ResultPath, ResultFileType):
        print("CreatExcelApp")
        ExcelBook = ExlCom(VBAFile, isVisible=ExcelVisible)
        print("ExecuVBAFunction")
        ExcelBook.RunVBA(VBAFunction)
        print("CloseExcelFile")
        ExcelBook.Close(SaveChanges=SaveChanges)  # 关闭excel，不保存
        if ResultPath == None:
            pass
        else:
            print("OpenResult")
            Infra.OpenFile('start', DaPr.FindNewestFileInWindows(ResultPath, ResultFileType), None)
        print("JobDone")

class ExlCom:
    """A utility to make it easier to get at Excel.    Remembering
    to Save the data is your problem, as is    error handling.
    Operates on one workbook at a time."""

    def __init__(self, filename=None, isVisible=None, isReadOnly=None, Format=None, Password=None,
                 WriteResPassword=None):  # 打开文件或者新建文件（如果不存在的话）
        import win32com.client
        import pythoncom
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

    def RunVBA(self, VBAFunction):
        strPara = self.xlBook.Name + VBAFunction
        status = self.xlApp.ExecuteExcel4Macro(strPara)
        # print(status)

    def Save(self, newfilename=None):  # 保存文件
        if newfilename:
            self.filename = newfilename
            self.xlBook.SaveAs(newfilename)
        else:
            self.xlBook.Save()

    def Close(self, SaveChanges):  # 关闭文件
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