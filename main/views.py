#coding=utf-8
from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib.messages import info, error
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, DetailView
#使用了通用视图  注意传递模板
from mezzanine.conf import settings
from mezzanine.generic.models import ThreadedComment
from mezzanine.utils.views import paginate

from .models import Link
from .utils import order_by_score  #返回queryset


class UserFilterView(ListView):
    """
    List view that puts a ``profile_user`` variable into the context,
    which is optionally retrieved by a ``username`` urlpattern var.
    If a user is loaded, ``object_list`` is filtered by the loaded
    user. Used for showing lists of links and comments.
    """

    def get_context_data(self, **kwargs):
        context = super(UserFilterView, self).get_context_data(**kwargs)
        try:
            username = self.kwargs["username"]
        except KeyError:
            profile_user = None
        else:
            users = User.objects.select_related("profile")
            lookup = {"username__iexact": username, "is_active": True}
            profile_user = get_object_or_404(users, **lookup)
            qs = context["object_list"].filter(user=profile_user)
            context["object_list"] = qs
        context["profile_user"] = profile_user
        context["no_data"] = ("暂无建议")
        return context


class ScoreOrderingView(UserFilterView):
    """
    List view that optionally orders ``object_list`` by calculated
    score. Subclasses must defined a ``date_field`` attribute for the
    related model, that's used to determine time-scaled scoring.
    Ordering by score is the default behaviour, but can be
    overridden by passing ``False`` to the ``by_score`` arg in
    urlpatterns, in which case ``object_list`` is sorted by most
    recent, using the ``date_field`` attribute. Used for showing lists
    of links and comments.
    """

    def get_context_data(self, **kwargs):
        context = super(ScoreOrderingView, self).get_context_data(**kwargs)
        qs = context["object_list"]
        context["by_score"] = self.kwargs.get("by_score", True)
        context["by_canteen"] = self.kwargs.get("by_canteen", False)
        context["canteen"] = self.kwargs.get("canteen", 'other')
        context["num"] = self.kwargs.get('num',0)  #0其实是用来作为false用
        context["solved"] = self.kwargs.get('solved',False)  #0其实是用来作为false用


            

        if context["by_score"]:
            '''全部按分数'''
            #默认所有数量
            qs = order_by_score(qs, self.score_fields, self.date_field)  #qs是queryset传递过去，返回queryset
            if context["num"]:
                #控制数量，通过url或者查询关键字 get 
                num=int(context["num"])
                qs=qs[0:num]

        else:
            #按时间，默认所有
            qs = qs.order_by("-" + self.date_field)
            #时间,控制数量
            if context["num"]:
                #控制数量，通过url或者查询关键字 get 
                num=int(context["num"])
                qs=qs[0:num]           
        #按餐厅
        if context["by_canteen"] :

            '''硬编码了，习惯不好，为了速度 dirty and quickly 核心逻辑：把if 当作开关'''
            qs = Link.objects.filter(canteen=context["canteen"])  #queryset
            if context["by_score"]:
                '''餐厅内部按分数'''
                qs = order_by_score(qs, self.score_fields, self.date_field)
                #餐厅，热度，数量
                if context["num"]:
                    num=int(context["num"])
                    qs=qs[0:num]            
            else:
                qs = qs.order_by("-" + self.date_field)
                #餐厅，时间，数量
                if context["num"]:
                    num=int(context["num"])
                    qs=qs[0:num]


        if context["solved"]:  #最后一步过滤,queryset是list,当作list来过滤
            #qs=qs.objects.filter(solved=True)
            qs = [item for item in qs if item.solved == False]

        context["object_list"] = paginate(qs, self.request.GET.get("page", 1),
            settings.ITEMS_PER_PAGE, settings.MAX_PAGING_LINKS)
        context["title"] = self.get_title(context)
        return context


class LinkView(object):
    """
    List and detail view mixin for links - just defines the correct
    queryset.
    """
    def get_queryset(self):
        return Link.objects.published().select_related("user", "user__profile")


class LinkList(LinkView, ScoreOrderingView):
    """
    List view for links, which can be for all users (homepage) or
    a single user (links from user's profile page). Links can be
    order by score (homepage, profile links) or by most recently
    created ("newest" main nav item).
    模板怎么传递
    """

    date_field = "publish_date"
    score_fields = ("rating_sum")# 统计分数 是个魔术方法 ("rating_sum", "comments_count")

    def get_title(self, context):
        if context["by_score"]:
            return ""  # Homepage
        if context["profile_user"]:
            return "建议 by %s" % context["profile_user"].profile
        else:
            return ""


class LinkCreate(CreateView):
    """
    Link creation view - assigns the user to the new link, as well
    as setting Mezzanine's ``gen_description`` attribute to ``False``,
    so that we can provide our own descriptions.
    """

    form_class = modelform_factory(Link, fields=("canteen","title",
                                                 "description"))
    model = Link

    def form_valid(self, form):
        '''
        hours = getattr(settings, "ALLOWED_DUPLICATE_LINK_HOURS", None)
        
        if hours:
            lookup = {
                "link": form.instance.link,
                "publish_date__gt": now() - timedelta(hours=hours),
            }
            
            try:
                link = Link.objects.get(**lookup)
            except Link.DoesNotExist:
                pass
            else:
                error(self.request, "Link exists")
                return redirect(link)
            '''
        form.instance.user = self.request.user
        form.instance.gen_description = False
        info(self.request, "建议 created")
        return super(LinkCreate, self).form_valid(form)


class LinkDetail(LinkView, DetailView):
    """
    Link detail view - threaded comments and rating are implemented
    in its template.
    """
    pass


class CommentList(ScoreOrderingView):
    """
    List view for comments, which can be for all users ("comments" and
    "best" main nav items) or a single user (comments from user's
    profile page). Comments can be order by score ("best" main nav item)
    or by most recently created ("comments" main nav item, profile
    comments).
    """
    #as view是哪个的函数  ，继承自哪里 只能是这里，来自这里from django.views.generic import ListView, CreateView, DetailView


    date_field = "submit_date"
    score_fields = ("rating_sum",)

    def get_queryset(self):#这个是重载  ，覆盖原理的方法 返回要求的接口数据就行
        return ThreadedComment.objects.visible().select_related("user",
            "user__profile").prefetch_related("content_object")

    def get_title(self, context):
        if context["profile_user"]:
            return "Comments by %s" % context["profile_user"].profile
        elif context["by_score"]:
            return "Best comments"  #这里就是高分排序的关键了
        else:
            return "Latest comments"

