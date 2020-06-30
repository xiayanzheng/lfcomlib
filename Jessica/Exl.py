from lfcomlib.Jessica import Infra
from lfcomlib.Jessica import DaPr


class Core:

    def __init__(self):
        self.excel_file = None

    def get_col_data_by_header(self, excel, sheet_name, head):
        import math, pandas
        # print(pandas.read_excel(excel,sheet_name='T-Commbox',index_col='CityCode'))
        excel_file = pandas.read_excel(excel, sheet_name=sheet_name)
        bucket = []
        # print(xl.to_dict())
        # print(xl.values.tolist())
        headers = []
        for Head in excel_file.keys():
            headers.append(Head)
        for Data in excel_file.get_values():
            print(Data)
            data = Data[headers.index(head)]
            try:
                math.isnan(data)
                pass
            except:
                bucket.append(data)
        return bucket

    def open_excel(self,excel_file_path):
        self.excel_file = ExlCom(filename=excel_file_path, is_readonly=False, is_visible=False)

    def close_excel(self):
        self.excel_file.close(0)

    def get_col_data_by_header_with_com(self, sheet_name, head, it_range, do_not_show_none):

        data_source = self.excel_file.get_range(sheet=sheet_name, col1=it_range[0], row1=it_range[1],
                                         col2=it_range[2], row2=it_range[3])
        # print(data_source)
        header_num = None
        data_set = []
        for each_row_of_data in data_source:
            # print(each_row_of_data)
            if header_num is None:
                each_row_of_data_list = []
                for Element in each_row_of_data:
                    # print(Element)
                    each_row_of_data_list.append(Element)
                if head in each_row_of_data_list:
                    header_num = each_row_of_data_list.index(head)
            else:
                if do_not_show_none:
                    if each_row_of_data[header_num] is None:
                        pass
                    else:
                        data_set.append(each_row_of_data[header_num])
                else:
                    data_set.append(each_row_of_data[header_num])
        return data_set

    def write_data_to_excel_sheet(self, excel, sheet_name, dataset):
        from openpyxl import load_workbook
        workbook = load_workbook(excel, read_only=False, keep_vba=True)
        selected_sheet = workbook[sheet_name]
        for data in dataset:
            selected_sheet[data['Cell']] = data['Data']
        workbook.save(excel)

    def vba_con(self, vba_file, vba_function, excel_visible, save_changes, result_path, result_file_type):
        print("CreatExcelApp")
        excel_book = ExlCom(vba_file, is_visible=excel_visible)
        print("Execute VBAFunction")
        excel_book.run_vba(vba_function)
        print("CloseExcelFile")
        excel_book.close(save_changes=save_changes)  # 关闭excel，不保存
        if result_path is None:
            pass
        else:
            print("OpenResult")
            Infra.open_file('start', DaPr.find_newest_file_in_windows(result_path, result_file_type), None)
        print("JobDone")


class ExlCom:
    """A utility to make it easier to get at Excel.    Remembering
    to Save the data is your problem, as is    error handling.
    Operates on one workbook at a time."""

    def __init__(self, filename=None, is_visible=None, is_readonly=None, exl_format=None, password=None,
                 write_res_password=None):  # 打开文件或者新建文件（如果不存在的话）
        import win32com.client
        import pythoncom
        pythoncom.CoInitialize()
        self.xlApp = win32com.client.Dispatch('Excel.Application')
        self.xlApp.Visible = is_visible
        if filename:
            self.filename = filename
            self.xlBook = self.xlApp.Workbooks.Open(filename, ReadOnly=is_readonly, Format=exl_format, Password=password,
                                                    WriteResPassword=write_res_password)
        else:
            self.xlBook = self.xlApp.Workbooks.Add()
            self.filename = ''

    def run_vba(self, vba_function_name,show_status=False):
        str_para = self.xlBook.Name + vba_function_name
        status = self.xlApp.ExecuteExcel4Macro(str_para)
        if show_status:
            print(status)

    def save(self, new_file_name=None):  # 保存文件
        if new_file_name is not None:
            self.filename = new_file_name
            self.xlBook.SaveAs(new_file_name)
        else:
            self.xlBook.save()

    def close(self, save_changes):  # 关闭文件
        self.xlBook.close(save_changes=save_changes)
        del self.xlApp
        # pythoncom.CoUninitialize()

    def get_cell(self, sheet, row, col):  # 获取单元格的数据
        # "get value of one cell"
        sht = self.xlBook.Worksheets(sheet)
        return sht.Cells(row, col).Value

    def set_cell(self, sheet, row, col, value):  # 设置单元格的数据
        # "set value of one cell"
        sheet = self.xlBook.Worksheets(sheet)
        sheet.Cells(row, col).Value = value

    def set_cell_format(self, sheet, row, col):  # 设置单元格的数据
        # "set value of one cell"
        open_sheet = self.xlBook.Worksheets(sheet)
        open_sheet.Cells(row, col).Font.Size = 15  # 字体大小
        open_sheet.Cells(row, col).Font.Bold = True  # 是否黑体
        open_sheet.Cells(row, col).Name = "Arial"  # 字体类型
        open_sheet.Cells(row, col).Interior.ColorIndex = 3  # 表格背景
        # sht.Range("A1").Borders.LineStyle = xlDouble
        open_sheet.Cells(row, col).BorderAround(1, 4)  # 表格边框
        open_sheet.Rows(3).RowHeight = 30  # 行高
        open_sheet.Cells(row, col).HorizontalAlignment = -4131  # 水平居中xlCenter
        open_sheet.Cells(row, col).VerticalAlignment = -4160  #

    def delete_row(self, sheet, row):
        sht = self.xlBook.Worksheets(sheet)
        sht.Rows(row).Delete()  # 删除行
        sht.Columns(row).Delete()  # 删除列

    def get_range(self, sheet, row1, col1, row2, col2):  # 获得一块区域的数据，返回为一个二维元组
        # "return a 2d array (i.e. tuple of tuples)"
        sht = self.xlBook.Worksheets(sheet)
        return sht.Range(sht.Cells(row1, col1), sht.Cells(row2, col2)).Value

    def add_picture(self, sheet, picture_name, left, top, width, height):  # 插入图片
        # "Insert a picture in sheet"
        sht = self.xlBook.Worksheets(sheet)
        sht.Shapes.add_picture(picture_name, 1, 1, left, top, width, height)

    def copy_sheet(self, before):  # 复制工作表
        # "copy sheet"
        sheets = self.xlBook.Worksheets
        sheets(1).Copy(None, sheets(1))

    def insert_row(self, sheet, row):
        sht = self.xlBook.Worksheets(sheet)
        sht.Rows(row).Insert(1)
