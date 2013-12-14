# -*- coding: utf-8 -*-
DEBUG =  False
TEMPLATE_DEBUG = False


SECRET_KEY = "jqx$20k4d^_c7zq9=m1dyuv-f_izs1r^s6pug=vdtwpq-b7o79"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "/home/wwj/xigua/dev.db",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

ALLOWED_HOSTS=['*']

#SEARCH_MODEL_CHOICES="pages.Page main.Link"

ACCOUNTS_PROFILE_FORM_EXCLUDE_FIELDS = (
    "first_name",
    "last_name",
    'website',
    'bio',
)

USE_I18N = True
LANGUAGE_CODE = 'zh'

#排除



#email
EMAIL_HOST = 'smtp.qq.com' 
EMAIL_PORT = 25
EMAIL_HOST_USER='2230360562@qq.com'  
EMAIL_HOST_PASSWORD='wwjtest'

BLOG_USE_FEATURED_IMAGE = True 
ACCOUNTS_ENABLED = True

PAGES_MENU_SHOW_ALL = False

