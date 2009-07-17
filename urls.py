from django.conf.urls.defaults import *
from models import Comic

urlpatterns = patterns('nr_comics.views',
    url(r'^$', "archive"),
    url(r'^(?P<slug>\d+)/$', 'comic'),
    url(r'^(?P<slug>\d+)/image/$', 'comic_image'),
)
