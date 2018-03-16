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


# 跟表格相关操作

def get_table(table_id):
    query_table = models.Table.objects.filter(pk=table_id)
    if query_table:
        table = query_table.first()
        return table
    return None
