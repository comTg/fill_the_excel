from django.db import models


# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=32, default='Title')
    content = models.TextField(null=True)

    def __str__(self):
        return self.title


class Table(models.Model):
    show = models.SmallIntegerField(default=0)
    title = models.TextField(null=False)
    expired = models.IntegerField(default=0)
    field = models.TextField()  # 字段
    allow_add = models.IntegerField(default=0)  # 是否允许输入多次内容
    allow_null = models.IntegerField(default=0)  # 是否允许为空

    def __str__(self):
        return self.title

# 使用cookie记住用户
class User(models.Model):
    token = models.TextField(null=False)
    counts = models.IntegerField(default=0)
    pub_time = models.DateTimeField(null=True)

class UserToTable(models.Model):
    token = models.TextField(null=False)
    rows = models.TextField(default=0) # 操作的行数,多行用,分开
    title = models.TextField(null=False)
    counts = models.IntegerField(default=0)
    pub_time = models.DateTimeField(null=True)


class PostCount(models.Model):
    ip = models.TextField(default=0)
    rows = models.IntegerField(default=0)
    title = models.TextField()
    counts = models.IntegerField(default=0)
    pub_time = models.DateTimeField(null=True)
