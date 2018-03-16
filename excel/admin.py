from django.contrib import admin

from .models import *


class PostCountAdmin(admin.ModelAdmin):
    list_display = (
        'ip',
        'title',
        'rows',
        'counts',
        'pub_time',
    )
    list_filter = ('pub_time', )


class TableAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'field', 'show', 'expired','allow_add')

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'token',
        'counts',
        'pub_time',
    )
    list_filter = ('pub_time',)

class UserToTableAdmin(admin.ModelAdmin):
    list_display = (
        'token',
        'title',
        'rows',
        'counts',
        'pub_time',
    )

admin.site.register(PostCount, PostCountAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(UserToTable,UserToTableAdmin)


# Register your models here.

# admin.site.register(Article)
