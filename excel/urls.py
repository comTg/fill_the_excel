from django.conf.urls import url, include
from django.views.generic import TemplateView

from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^table/$', views.get_excel,name="table"),
    url(r'^post$', views.form_action,name="post_table"),
    url(r'^table/(?P<table_id>[0-9]+)$', views.get_excel,name="get_table"),
    url(r'^download/$', views.get_file,name="download"),
    url(r'^download/(?P<file>.+)$', views.download_excel,name="download_file"),
    # url(r'^login/$',TemplateView.as_view(template_name="excel\login.html"),name="login"),
    url(r'^login/$',views.LoginView.as_view(),name="login"),
    url(r'^modify/$',views.modify,name='modify'),
    url(r'^api/getexcel/$',views.get_content,name="get_content"),
    url(r'^api/gettitle/$',views.get_title,name="get_title"),
    url(r'^api/change/$',views.change_table,name="change_table"),

]
