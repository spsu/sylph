from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.apps.post.views',
	(r'^$', 'index_parentless'),
	(r'^all/$', 'index_all'),
	(r'create/$', 'create_post'),
	(r'view/(?P<post_id>\d+)/$', 'view_post'),
	(r'reply/(?P<post_id>\d+)/$', 'reply_post'),
	(r'delete/(?P<post_id>\d+)/$', 'delete_post'),
)

