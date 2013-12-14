#coding=utf-8


from django.conf.urls import patterns, url

from django.views.generic.simple import direct_to_template
from main.views import LinkList


urlpatterns = patterns("",
    (r'^aboutus/$', direct_to_template, {'template': 'aboutus.html'}),
    (r'^messageboard/$', direct_to_template, {'template': 'messageboard.html'}),
    (r'^hwh/$', direct_to_template, {'template': 'hwh.html'}),
    #打印报表
    (r'^report/$', direct_to_template, {'template': 'report.html'}),#放在用户页面那里比较好
	url("^reportform/$",
        LinkList.as_view(template_name='reportform.html'), #看一下返回什么 把函数视为传参  模板里怎么用 模板是 link list
        ),
 #调用main的打印函数？主体用他们 具体而言好事得自己写函数
#使用一个公共的东西来获取渲染

#餐厅 最佳  例如 http://127.0.0.1:7000/onepage/reportform/canteen/hc/2/  回餐最热前二,给个开关就是最新前二
    #all
    url("^reportform/canteen/newest/(?P<num>\d*)/$",
        LinkList.as_view(template_name='reportform.html'), #看一下返回什么 把函数视为传参  模板里怎么用 模板是 link list
        ),
    url("^reportform/canteen/(?P<num>\d*)/$",
        LinkList.as_view(template_name='reportform.html'),{"by_score":True,"solved":True} #看一下返回什么 把函数视为传参  模板里怎么用 模板是 link list
        ),


    url("^reportform/canteen/(?P<canteen>\w*)/(?P<num>\d*)/$",
        LinkList.as_view(template_name='reportform.html'),{"by_canteen":True,"solved":True} #看一下返回什么 把函数视为传参  模板里怎么用 模板是 link list
        ),
    #时间最新
    url("^reportform/canteen/newest/(?P<canteen>\w*)/(?P<num>\d*)/$",
        LinkList.as_view(template_name='reportform.html'),{"by_canteen":True,"by_score": False,"solved":True}, #看一下返回什么 把函数视为传参  模板里怎么用 模板是 link list
        ),

)


'''
from main.views import LinkList

最热
url("^reportform/$",
        LinkList.as_view(template_name='reportform.html'), 看一下返回什么 把函数视为传参  模板里怎么用 模板是 link list
        name="print_list_best"),
'''