from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.core.feed.views',
	(r'^/$', 'index'),
)

