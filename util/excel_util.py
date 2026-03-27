# # coding=utf-8
# import csv  # 添加CSV处理模块
# import xlrd
# from xlutils.copy import copy
# import time
#
#
# class ExcelUtil:
#     def __init__(self, excel_path=None, index=None):
#         self.excel_path = excel_path
#         self.is_csv = False
#
#         if excel_path is None:
#             self.excel_path = "E:\\Teacher\\Imooc\\SeleniumPython\\config\\casedata.xls"
#         else:
#             # 检查文件扩展名判断是否为CSV
#             if excel_path.lower().endswith('.csv'):
#                 self.is_csv = True
#
#         if not self.is_csv:
#             # 处理Excel文件
#             if index is None:
#                 index = 0
#             self.data = xlrd.open_workbook(self.excel_path)
#             self.table = self.data.sheets()[index]
#         else:
#             # 处理CSV文件
#             self.data = []
#             try:
#                 with open(self.excel_path, 'r', encoding='utf-8') as f:
#                     reader = csv.reader(f)
#                     self.data = list(reader)
#             except Exception as e:
#                 print(f"读取CSV文件时出错: {e}")
#
#     # 获取数据
#     def get_data(self):
#         if self.is_csv:
#             return self.data
#         else:
#             result = []
#             rows = self.get_lines()
#             if rows is not None:
#                 for i in range(rows):
#                     col = self.table.row_values(i)
#                     result.append(col)
#                 return result
#             return None
#
#     # 获取行数
#     def get_lines(self):
#         if self.is_csv:
#             return len(self.data) if self.data else 0
#         else:
#             rows = self.table.nrows
#             if rows >= 1:
#                 return rows
#             return None
#
#     # 获取单元格数据
#     def get_col_value(self, row, col):
#         if self.is_csv:
#             if 0 <= row < len(self.data) and 0 <= col < len(self.data[row]):
#                 return self.data[row][col]
#             return None
#         else:
#             if self.get_lines() > row:
#                 data = self.table.cell(row, col).value
#                 return data
#             return None
#
#     # 写入数据 (注意：CSV文件的写入逻辑与Excel不同)
#     def write_value(self, row, value):
#         if self.is_csv:
#             # 读取CSV文件内容
#             data = []
#             try:
#                 with open(self.excel_path, 'r', encoding='utf-8') as f:
#                     reader = csv.reader(f)
#                     data = list(reader)
#             except Exception as e:
#                 print(f"读取CSV文件时出错: {e}")
#                 return
#
#             # 确保有足够的行
#             while len(data) <= row:
#                 data.append([])
#
#             # 添加或更新值
#             if len(data[row]) <= 9:
#                 data[row].extend([None] * (10 - len(data[row])))
#             data[row][9] = value
#
#             # 写入CSV文件
#             try:
#                 with open(self.excel_path, 'w', encoding='utf-8', newline='') as f:
#                     writer = csv.writer(f)
#                     writer.writerows(data)
#                 time.sleep(1)
#             except Exception as e:
#                 print(f"写入CSV文件时出错: {e}")
#         else:
#             # 原有的Excel写入逻辑
#             read_value = xlrd.open_workbook(self.excel_path)
#             write_data = copy(read_value)
#             write_data.get_sheet(0).write(row, 9, value)
#             write_data.save(self.excel_path)
#             time.sleep(1)
#
#
# if __name__ == '__main__':
#     # 示例：处理CSV文件
#     ex = ExcelUtil('../config/acoountdata.csv')
#     print(ex.get_col_value(0, 0))
#
#     # 示例：处理Excel文件
#     # ex = ExcelUtil('path/to/your/file.xls')
#     # print(ex.get_col_value(0, 0))