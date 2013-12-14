# -*- coding: utf-8 -*-
from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin
from .models import Link


class LinkAdmin(DisplayableAdmin):
#控制后台
    list_display = ("id",'canteen', "title",  "publish_date",
                     "rating_sum",'solved')
    list_display_links = ("id",)
    list_editable = ("title",'canteen','solved')
    list_filter = ("status", "user__username")
    ordering = ("-publish_date",)

    fieldsets = (
        (None, {
            "fields": ("title",'canteen', "publish_date", "user"),
        }),
    )


admin.site.register(Link, LinkAdmin)
