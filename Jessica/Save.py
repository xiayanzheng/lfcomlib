import copy
import csv
import os
import xlrd

from xlwt import Style
from lfcomlib.Jessica import Msg
from lfcomlib.Jessica import ErrMsg

Msg = Msg.Core()


class Core:

    @staticmethod
    def to_csv(headers, data, *args, show_status=False):
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
        return True

    @staticmethod
    def to_csv_single_row(csv_, headers_, data_):
        # 定义Writer对象(由CSV.DictWriter(以字典模式写入)模块组成并定义列名称)
        writer = csv_.DictWriter(csv_, fieldnames=headers_)
        # 写入列名称(字典的键)
        writer.writeheader()
        # 写入元素(字典的值)
        writer.writerow(data_)
        # print(Msg.WriteDataSuccess)
        csv_.close()

    @staticmethod
    def to_txt(file_path, file_name, data):
        # 定义文件路径
        log_path = os.path.join(file_path, file_name)
        # 打开文件
        with open(log_path, 'w', encoding='utf-8') as Log:
            # 写入数据
            Log.write(data)
            # 输出"写入数据成功数据"
            # 打开数据存储文件夹
        return log_path

    @staticmethod
    def to_xls(self, file, row, col, str_, style_=Style.default_style):
        # 合并单元格:
        # ws.write_merge(top_row, bottom_row, left_column, right_column, string)
        rb = xlrd.open_workbook(file, formatting_info=True)
        wb = copy(rb)
        ws = wb.get_sheet(0)
        ws.write(row, col, str_, style_)
        wb.save(file)

    @staticmethod
    def modify_excel(self, file_path, file_name, row_col_set, data):
        book = xlrd.open_workbook(file_name)  # 打开excel
        new_book = copy(book)  # 复制excel
        sheet = new_book.get_sheet(0)  # 获取第一个表格的数据
        for RowCol in row_col_set:
            sheet.write(RowCol[0], RowCol[1], data)  # 修改0行1列的数据为'Haha'
        temp_file = os.path.join(file_path, 'Temp.xls')
        new_book.save(temp_file)  # 保存新的excel
        try:
            os.remove(file_name)  # 删除旧的excel
            os.rename(temp_file, file_name)  # 将新excel重命名
        except Exception as e:
            print(e)
            print(ErrMsg.UnableAccessThisFile)
