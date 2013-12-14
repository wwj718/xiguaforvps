#coding=utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin

from mezzanine.core.views import direct_to_template


admin.autodiscover()


urlpatterns = patterns("",
    ("^admin/", include(admin.site.urls)),
    ("^", include("main.urls")),  #优先,可覆盖
    ("^", include("mezzanine.urls")),  #page
    ("^onepage/", include("onepage.urls")),  #page


)

# Adds ``STATIC_URL`` to the context.
handler500 = "mezzanine.core.views.server_error"
