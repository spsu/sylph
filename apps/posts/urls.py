from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.apps.posts.views',
	# Endpoint
	(r'^$', 'indexParentless'),
	(r'^all/$', 'indexAll'),
	(r'create/$', 'createPost'),
	(r'view/(?P<postId>\d+)/$', 'viewPost'),
	(r'reply/(?P<postId>\d+)/$', 'replyPost'),
	(r'delete/(?P<postId>\d+)/$', 'deletePost'),

)

# Okay, this is all great, but it does nothing if I can't send it somewhere.
