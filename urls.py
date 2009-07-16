from django.conf.urls.defaults import *

from django.views.generic.list_detail import object_list
from models import Comic

urlpatterns = patterns('nr_comics.views',
    url(r'^$', "archive"),
    url(r'^(?P<slug>\d+)/$', 'comic'),
    url(r'^(?P<slug>\d+)/image/$', 'comic_image'),
)
