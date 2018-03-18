import os

import xlrd
import xlwt
from xlutils.copy import copy
from WordTo_Excel.settings import BASE_DIR
from collections import OrderedDict
from django.utils import timezone
from cryptography.fernet import Fernet
from . import dev

SALT = b'ri8dodgnexBkEcpuRc1KvXTCNzsFHYuv-BRhfi0BPo8='
SALT_TG = 'test/salt'
MAX_AGE = 5000 * 24 * 60
ROW_WIDTH = 6000



def validate_cookie(request):  # 根据传入request判断是否含有cookie
    if 'data' in request.COOKIES:
        data = request.COOKIES['data']
        # result = decrypt_data(data)  # 解密cookie
        # results = result.split(',')
        # data = request.get_signed_cookie('data',salt=SALT_TG);
        return data
    else:
        return None


def add_cookie(response, ip):
    time_now = timezone.now()
    data = '{ip},{time}'.format(ip=ip, time=time_now)
    token = encrypt_data(data)
    response.set_cookie('data', token, max_age=MAX_AGE)
    # response.set_signed_cookie('data',data,salt=SALT_TG)
    return response, token


def encrypt_data(data):
    d = data.encode('utf-8')  # 转换字符串格式
    f = Fernet(SALT)  # 通过盐值生成加密解密端
    token = f.encrypt(d)
    token = token.decode('utf-8')  # 返回转换成字符串的结果
    return token


def decrypt_data(data):
    token = data.encode('utf-8')
    f = Fernet(SALT)
    data = f.decrypt(token)
    data = data.decode('utf-8')  # 解码并转换成字符串
    return data


# -----------------

def get_style(is_title=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = "微软雅黑"
    font.height = 240
    if is_title:
        font.height = 350
        dev.log(font=font.height)
    style.font = font
    # style.alignment.wrap = 1
    return style


def get_file_path(title):
    file_path = os.path.join(BASE_DIR, '{title}.{suffix}'.format(title=title, suffix='xls'))
    return file_path;

def overwrited_title(sheet,title,fields):
    style = get_style(True)
    sheet.write(0,0,title,style)
    column_count = 0
    for field in fields:
        sheet.col(column_count).width = ROW_WIDTH
        sheet.write(1, column_count, field, style)
        column_count += 1


def new_excel(title, fields):
    try:
        file_path = get_file_path(title)
        if os.path.exists(file_path):
            print('{}-已存在'.format(file_path))
            return
        book = xlwt.Workbook()
        sheet1 = book.add_sheet('Sheet1')
        overwrited_title(sheet1,title,fields)
        book.save(file_path)
        dev.log(succ='新建{}成功!'.format(file_path))
    except Exception as e:
        dev.log(err=str(e),tips="新建{}失败".format(file_path))


def open_excel(title):
    try:
        file_path = get_file_path(title)
        data = xlrd.open_workbook(file_path)
        return data
    except Exception as e:
        print(str(e), '打开excel发生错误')


def read_from_excel(title):
    file_path = get_file_path(title)
    if os.path.exists(file_path):
        data = open_excel(title)
        table = data.sheet_by_name('Sheet1')
        row_two = table.row_values(1)  # 获得第二行内容
        results = []
        for rownum in range(2, table.nrows):
            row = table.row_values(rownum)  # 根据行号获取行
            if row:
                rows = OrderedDict()
                for i in range(len(row)):
                    key = row_two[i]
                    if isinstance(key, float):
                        key = int(key)
                    if key == '':
                        key = str(i)
                    rows[key] = row[i]
                results.append(rows)
        results.reverse()  # 倒序传回前端页面显示
        return results
    else:
        return None


def read_one_row(title, row):
    file_path = get_file_path(title)
    if os.path.exists(file_path):
        data = open_excel(title)
        table = data.sheet_by_name('Sheet1')
        one_row = table.row_values(row)  # 获得第row+1行的内容
        return one_row
    else:
        return None

def init_sheet(title,fields):
    file_path = get_file_path(title)
    style = get_style()
    data = open_excel(title)  # 打开excel文件
    table = data.sheet_by_name('Sheet1')  # 打开表
    nrows = table.nrows  #  获得行数
    book = copy(data)
    sheet1 = book.get_sheet(0)
    overwrited_title(sheet1,title,fields)
    return sheet1,book,file_path,nrows,style

def write_to_excel(title, fields,results, rows, change_row, allow_add):
    is_change = False
    try:
        sheet1,book,file_path,nrows,style = init_sheet(title,fields)
        column_count = 0
        rows_list = str(rows).split(',')
        if allow_add or int(rows_list[0]) == 0:  # 判断该表格是否允许相同用户重复添加
            mark_row = nrows
        else:
            mark_row = int(rows_list[0])
        #  判断是否在列表中
        dev.log(change_row=change_row, rows_list=rows_list)
        if str(change_row) != '0' and str(change_row) in rows_list:
            mark_row = int(change_row)
            is_change = True
        for value in results:
            sheet1.write(mark_row, column_count, value,style)
            column_count += 1
        book.save(file_path)
        dev.log(success="数据保存到excel成功!")
        return mark_row, is_change
    except Exception as e:
        dev.log(error='保存数据到excel时发生错误',err=str(e))

def write_all_rows(title,fields,results):
    try:
        sheet1,book,file_path,nrows,style = init_sheet(title,fields)
        style = get_style()
        row_count = 2
        row_keys = list(results.keys())
        row_keys.reverse()
        for one_row in row_keys:
            column_count = 0
            row_value = results[one_row]
            for td in row_value:
                sheet1.write(row_count,column_count,row_value[td],style)
                column_count += 1
            row_count += 1
        book.save(file_path)
        dev.log(succ="数据更新到excel成功")
    except Exception as e:
        dev.log(err=str(e))

if __name__ == '__main__':
    # title = '测试标题-test'
    # results = read_one_row(title, 2)
    # print(results)

    token = encrypt_data('唐刚')
    result = decrypt_data(str(token))
    print(result)
