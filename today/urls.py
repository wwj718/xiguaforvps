#coding=utf-8


from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import LinkList, LinkCreate, LinkDetail, CommentList


urlpatterns = patterns("",
    url("^$",
        LinkList.as_view(),
        name="home"),
    url("^newest/$",
        LinkList.as_view(), {"by_score": False},
        name="link_list_latest"),   #按分数排序如此简单，有接口，不添加false就行
    
    url("^suggestions/best/$",
        LinkList.as_view(), 
        name="link_list_best"),

#按餐厅排序
    url("^canteen/(?P<canteen>.*)/$", #可选canteen/sc 参考models 
        LinkList.as_view(), {"by_canteen":  True},
        name="link_list_canteen"),

    url("^comments/$",
        CommentList.as_view(), {"by_score": False},
        name="comment_list_latest"),
    url("^best/$",
        CommentList.as_view(),
        name="comment_list_best"),

    url("^link/create/$",
        login_required(LinkCreate.as_view()),
        name="link_create"),
    url("^link/(?P<slug>.*)/$",
        LinkDetail.as_view(),
        name="link_detail"),
    url("^users/(?P<username>.*)/links/$",
        LinkList.as_view(), {"by_score": False},
        name="link_list_user"),
    url("^users/(?P<username>.*)/links/$",
        LinkList.as_view(), {"by_score": False},
        name="link_list_user"),
    url("^users/(?P<username>.*)/comments/$",
        CommentList.as_view(), {"by_score": False},
        name="comment_list_user"),
)
