# -*- coding:utf-8 -*-
import xlrd
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ os.path.sep+"files"
xlsfile = os.path.join(parent_dir, 'IPList.xlsx')

class Read_Excel():

    def get_ip(self):
        book = xlrd.open_workbook(xlsfile)  # 调用xlrd，打开Excel文件
        sheet = book.sheet_by_index(0)  # 通过索引，获取相应的列表，这里表示获取Excel第一个sheet
        city_IP = sheet.col_values(2)
        for i in city_IP:
            return city_IP

if __name__ == "__main":
    Read_Excel().get_ip(xlsfile)