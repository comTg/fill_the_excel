from django.test import TestCase

import xlwt

# Create your tests here.

def get_style(is_title=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = "微软雅黑"
    font.height = 270
    if is_title:
        font.height = 400
    style.font = font
    # style.alignment.wrap = 1
    return style

def create_xls():
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('Sheet1')
    style = get_style(True)
    sheet1.write(0,0,'test',style)
    for i in range(5):
        sheet1.col(i).width = 5000
        sheet1.write(1,i,'t刚刚',style)
    book.save('test.xls')

if __name__ == '__main__':
    create_xls()


