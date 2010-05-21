from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.apps.posts.views',
	# Endpoint
	(r'^/?$', 'index'),
	(r'create/$', 'createPost'),
	(r'view/(?P<postId>\d+)/$', 'viewPost'),
	(r'delete/(?P<postId>\d+)/$', 'deletePost'),

)

# Okay, this is all great, but it does nothing if I can't send it somewhere.
