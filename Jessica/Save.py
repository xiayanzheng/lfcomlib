import os, csv, xlrd, copy
from xlwt import Style
from lfcomlib.Jessica import Msg

Msg = Msg.Core()

class Core:

    def toCSV(self, headers, data,*args,show_status=False):
        if len(args) > 1:
            file_path, file_name = args[0], args[1]
            file_path = os.path.join(file_path, file_name)
        else:
            file_path = args[0]
        if show_status:
            print("S")
        with open(file_path, 'w', newline='') as CSV:
            # 定义Writer对象(由CSV.DictWriter(以字典模式写入)模块组成并定义列名称)
            handler = csv.DictWriter(CSV, fieldnames=headers)
            # 写入列名称(字典的键)
            handler.writeheader()
            # 循环写入列表中每一条数据到CSV文件
            for Row in data:
                if show_status:
                    print(Row)
                # 写入元素(字典的值)
                handler.writerow(Row)
        if show_status:
            print(Msg.WriteDataSuccess)
        CSV.close()

    def toCSVSR(self, CSV, Headers, Data):
        # 定义Writer对象(由CSV.DictWriter(以字典模式写入)模块组成并定义列名称)
        Writer = csv.DictWriter(CSV, fieldnames=Headers)
        # 写入列名称(字典的键)
        Writer.writeheader()
        # 写入元素(字典的值)
        Writer.writerow(Data)
        # print(Msg.WriteDataSuccess)
        CSV.close()

    def toTXT(self, FilePath, FileName, Data):
        # 定义文件路径
        LogPath = os.path.join(FilePath, FileName)
        # 打开文件
        with open(LogPath, 'w', encoding='utf-8') as Log:
            # 写入数据
            Log.write(Data)
            # 输出"写入数据成功数据"
            # 打开数据存储文件夹
        return LogPath

    def toXls(self, File, Row, Col, Str, Style=Style.default_style):
        # 合并单元格:
        # ws.write_merge(top_row, bottom_row, left_column, right_column, string)
        rb = xlrd.open_workbook(File, formatting_info=True)
        wb = copy(rb)
        ws = wb.get_sheet(0)
        ws.write(Row, Col, Str, Style)
        wb.save(File)

    def ModifyExcel(self, FilePath, Filename, RowColSet, Data):
        book = xlrd.open_workbook(Filename)  # 打开excel
        new_book = copy(book)  # 复制excel
        sheet = new_book.get_sheet(0)  # 获取第一个表格的数据
        for RowCol in RowColSet:
            sheet.write(RowCol[0], RowCol[1], Data)  # 修改0行1列的数据为'Haha'
        TempFile = os.path.join(FilePath, 'Temp.xls')
        new_book.save(TempFile)  # 保存新的excel
        try:
            os.remove(Filename)  # 删除旧的excel
            os.rename(TempFile, Filename)  # 将新excel重命名
        except:
            print(ErrMsg.UnableAccessThisFile)
