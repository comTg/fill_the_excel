import os
import json
from copy import deepcopy
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone
from django.http import StreamingHttpResponse
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from . import models
from . import tools
from . import userimpl
from . import dev
from .entity import TableInfo
from WordTo_Excel.settings import BASE_DIR


# Create your views here.


def index(request):
    template = loader.get_template('excel/index.html')
    # ----------- 获得所有的table
    tables = models.Table.objects.all()
    tableinfos = list()
    for table in tables:
        expired = True if table.expired == 1 else False
        t = TableInfo(table.id, table.title, expired)
        tableinfos.append(t)
    context = {
        'tableinfos': tableinfos,
    }
    response = HttpResponse(template.render(context, request))
    return response


def get_excel(request, table_id=1):
    template = loader.get_template('excel/table.html')
    table = userimpl.get_table(table_id)
    if table:
        # --------- 判断用户是否写入过数据
        is_first = True
        # 判断当前用户浏览器是否有cookie
        token = tools.validate_cookie(request)
        rows = 0
        if token:  # 持有cookie
            user = userimpl.get_user(token)
            if user:
                is_first = False
                user_table = userimpl.query_user_table(token, table.title)
                if user_table:
                    rows = user_table.rows
        # -----------
        #  是否显示填写好的内容
        is_show = True if table.show == 1 else False
        #  是否已经过期
        expired = True if table.expired == 1 else False
        #  是否允许填空值
        allow_null = '  ' if table.allow_null == 1 else ''  # 是否允许为空
        #  是否允许重复填写
        allow_add = True if table.allow_add == 1 else False
        if expired:
            return HttpResponse('<h2>该表格已过期</h2>')
        else:
            exists_value = tools.read_from_excel(table.title) if is_show else None
            fields = table.field.split(',')
            context = {
                'table_id': table_id,
                'title': table.title,
                'isShow': is_show,
                'value': fields,
                'allow_null': allow_null,
                'allow_add': allow_add,
                'exists_value': exists_value,
                'rows': rows,
            }
            response = HttpResponse(template.render(context, request))
            if is_first:
                ip = userimpl.get_ip(request)
                response, token = tools.add_cookie(response, ip)
                userimpl.add_user(token)
            return response
    else:
        return HttpResponse("<h2>目前暂时没有表格!</h2>")


def form_action(request):
    template = loader.get_template('excel/result.html')
    #  获得用户传过来的表单内容
    items = request.POST.items()
    ip = userimpl.get_ip(request)
    post_item = dict(items)
    table_id = 1
    try:  # 捕获未获取到id异常
        table_id = post_item['hidden_id']
        #  判断当前用户是否修改字段
        change_row = post_item['change_row']
        dev.log(ch=change_row)
        table = userimpl.get_table(table_id)  # 获得表格
        fields = table.field.split(',')  # 获得表格字段
        # 判断当前用户浏览器是否有cookie
        token = tools.validate_cookie(request)
        user = userimpl.get_user(token)
        if user:
            # 获得用户与该表格的关系
            user_table = userimpl.query_user_table(token, table.title)
            if user_table is None:
                user_table = userimpl.add_user_table(token, table.title)
            allow_add = True if table.allow_add == 1 else False
            tools.new_excel(table.title, fields)
            get_list = list()  # 使用列表传递字段和对应的表单值
            for i in range(len(fields)):
                get_list.append(post_item[fields[i]])
            mark_rows, is_change = tools.write_to_excel(table.title, fields, get_list, user_table.rows, change_row,
                                                        allow_add)
            dev.log(mark_rows=mark_rows)
            result_info = '提交成功'
            user_table.pub_time = timezone.now()
            dev.log(is_change=is_change)
            if str(user_table.rows) == '0' and not is_change:
                user_table.rows = mark_rows
            elif not is_change:
                user_table.rows = "{},{}".format(user_table.rows, mark_rows)
            user_table.counts += 1
            user_table.save()
            # 保存该ip操作记录
            mark_ip = userimpl.add_ip(ip, table.title)
            mark_ip.counts += 1
            mark_ip.save()
        else:
            result_info = '请按流程提交表单!'
    except Exception:
        result_info = '发生未知错误!'
    context = {
        'result_info': result_info,
        'table_id': table_id,
    }
    return HttpResponse(template.render(context, request))


def get_file(request):
    template = loader.get_template('excel/download.html')
    tables = models.Table.objects.all()
    titles = list()
    for table in tables:
        titles.append(table.title)
    context = {
        'titles': titles,
    }
    return HttpResponse(template.render(context, request))


def download_excel(request, file):
    file_path = os.path.join(BASE_DIR, file)

    def file_iterator(file_path, chunk_size=512):
        with open(file_path, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(file_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename={0}'.format(file)
    return response


class LoginView(View):
    def get(self, request):
        return render(request, "excel/login.html", {})

    def post(self, request):
        user = userimpl.validate_login(request)
        if user is not None:
            return redirect('/modify')
        else:
            return render(request, "excel/login.html", {"result": "用户名或密码错误"})


@login_required
def modify(request):
    return render(request, 'excel/modify_excel.html', {})

@login_required
def get_title(request):
    tables = models.Table.objects.all()
    titles = list()
    for table in tables:
        titles.append(table.title)
    result = json.dumps(titles,ensure_ascii=False)
    dev.log(get_title=result)
    return HttpResponse(result)

@login_required
def get_content(request):
    title = request.GET.get('title', '')
    exists_value = tools.read_from_excel(title)
    exists_value = json.dumps(exists_value,ensure_ascii=False)
    dev.log(value=exists_value)
    return HttpResponse(exists_value)

@csrf_exempt
@login_required()
def change_table(request):
    if request.method == "POST":
        data = request.POST.get("data","")
        title = request.POST.get("title","")
        data = json.loads(data)  # dict
        fields = userimpl.get_fields(title)
        dev.log(data=data,title=title,type=type(data))
        tools.write_all_rows(title,fields,data)
        return HttpResponse("ok");
    else:
        return HttpResponse("请使用post方式请求")


