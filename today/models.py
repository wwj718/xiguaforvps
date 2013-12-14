#coding=utf-8
from time import time
from urlparse import urlparse

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from mezzanine.core.models import Displayable, Ownable
from mezzanine.generic.models import Rating
from mezzanine.generic.fields import RatingField, CommentsField

class Link(Displayable, Ownable):
    c=(('hc','清真餐厅'),('yc','一餐厅'),('ec','二餐厅'),('sc','三餐厅'),('jby','聚博园'),('other','未分类'))
    canteen=models.CharField(max_length=20,choices=c,default='ec')
    link = models.URLField(blank=True)   #这个根本不需要，不要删除吧，免得麻烦，只要不让它出现就行,完成
    rating = RatingField()
    comments = CommentsField()
    solved  = models.BooleanField(default=False)
    
    @models.permalink
    def get_absolute_url(self):
        return ("link_detail", (), {"slug": self.slug})

    @property
    def domain(self):
        return urlparse(self.link).netloc


class Profile(models.Model):

    user = models.OneToOneField("auth.User")
    website = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    karma = models.IntegerField(default=0, editable=False)

    def __unicode__(self):
        return "%s (%s)" % (self.user, self.karma)


@receiver(post_save, sender=Rating)
def karma(sender, **kwargs):
    """
    Each time a rating is saved, check its value and modify the
    profile karma for the related object's user accordingly.
    Since ratings are either +1/-1, if a rating is being edited,
    we can assume that the existing rating is in the other direction,
    so we multiply the karma modifier by 2.
    """
    rating = kwargs["instance"]
    value = int(rating.value)
    if not kwargs["created"]:
        value *= 2
    content_object = rating.content_object
    if rating.user != content_object.user:
        queryset = Profile.objects.filter(user=content_object.user)
        queryset.update(karma=models.F("karma") + value)
