#coding=utf-8


from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from .views import LinkList, LinkCreate, LinkDetail, CommentList


urlpatterns = patterns("",
    url("^$",
        LinkList.as_view(),
        name="home"),
    #按时间排序
    url("^newest/$",
        LinkList.as_view(), {"by_score": False},
        name="link_list_latest"),   #按分数排序如此简单，有接口，不添加false就行
    
    # #按时间排序,限制数量,知道有num才被插触发
    # url("^newest/(?P<num>.*)$",
    #     LinkList.as_view(), {"by_score": False},#二选一的开关,要么时间要么热度
    #     name="link_list_latest"),   #按分数排序如此简单，有接口，不添加false就行
  

    #短路原则 ， 除非有数字不然先用全部
    url("^suggestions/best/$",
        LinkList.as_view(), 
        name="link_list_best"),
    #数量限制,print用
    # url("^suggestions/best/(?P<num>.*)$",
    #     LinkList.as_view(), 
    #     name="link_list_best"),


#按餐厅排序
    url("^canteen/(?P<canteen>\w*)/$", #注意. 它会截掉所有东西  可选canteen/sc 参考models 
        LinkList.as_view(), {"by_canteen":True,},
        name="link_list_canteen"),
#按餐厅排序，数量获取
    # url("^canteen/(?P<canteen>\w*)/(?P<num>.*)/$", #可选canteen/sc 参考models 
    #     LinkList.as_view(), {"by_canteen":True,},
    #     ),

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
