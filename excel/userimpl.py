from . import models
from django.utils import timezone


# 跟用户相关操作

def get_user(token):
    query_user = models.User.objects.filter(token=token)  # return QuerySet()
    if query_user:
        user = query_user.first()
        return user
    return None


def add_user(token, counts=0):
    pub_time = timezone.now()
    user = get_user(token)
    if user is None:
        user = models.User.objects.create(token=token,
                                   counts=counts,
                                   pub_time=pub_time)
    return user

def query_user_table(token,title):
    query_result = models.UserToTable.objects.filter(token=token,title=title)
    if query_result:
        result = query_result.first()
        return result
    return None

def add_user_table(token,title,rows=0,counts=0,pub_time=None):
    if pub_time is None:
        pub_time = timezone.now()
    result = query_user_table(token,title)
    if result is None:
        result = models.UserToTable.objects.create(token=token,
                                          title=title,
                                          rows=rows,
                                          counts=counts,
                                          pub_time=pub_time)
    return result

def query_ip(ip,title):
    query_result = models.PostCount.objects.filter(ip=ip,title=title)
    if query_result:
        result = query_result.first()
        return result
    return None

def add_ip(ip,title,counts=0,pub_time = None):
    if pub_time is None:
        pub_time = timezone.now()
    result = query_ip(ip,title)
    if result is None:
        result = models.PostCount.objects.create(ip=ip,
                                                 title=title,
                                                 counts=counts,
                                                 pub_time=pub_time)
    return result

#  获得访问者ip

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# 跟表格相关操作

def get_table(table_id):
    query_table = models.Table.objects.filter(pk=table_id)
    if query_table:
        table = query_table.first()
        return table
    return None
