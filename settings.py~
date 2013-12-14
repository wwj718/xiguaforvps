#coding:utf-8
from mezzanine.project_template.settings import *
import os

# Paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]
#STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))
STATIC_ROOT = '/home/wwj/xigua/statics'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))
ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME
TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)

INSTALLED_APPS = (
    "main",
    'onepage',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.accounts",  #需要微调啊,使用接口而不是自己侵入改


)

MIDDLEWARE_CLASSES = (["mezzanine.core.middleware.UpdateCacheMiddleware"] +
                      list(MIDDLEWARE_CLASSES) +
                      ["mezzanine.core.middleware.FetchFromCacheMiddleware"])
MIDDLEWARE_CLASSES.remove("mezzanine.pages.middleware.PageMiddleware")

# Mezzanine mezzanine部分
AUTH_PROFILE_MODULE = "main.Profile"
SITE_TITLE = "  GreenLine"  #站点名称
RATINGS_RANGE = (0, 1)
RATINGS_ACCOUNT_REQUIRED = True  #登录后可投票
COMMENTS_ACCOUNT_REQUIRED = True  #登录后可评论
ACCOUNTS_PROFILE_VIEWS_ENABLED = True  

ADMIN_MENU_ORDER = (
    ("Content", ("main.Link", "pages.Page", "blog.BlogPost",
       "generic.ThreadedComment", ("Media Library", "fb_browse"),)),
    ("Site", ("sites.Site", "redirects.Redirect", "conf.Setting")),
    ("Users", ("auth.User", "auth.Group",)),
)

# Drum
ALLOWED_DUPLICATE_LINK_HOURS = 24 * 7 * 3
ITEMS_PER_PAGE = 20  #分页参数，每页显示

try:
    from local_settings import *
except ImportError:
    pass

try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())

