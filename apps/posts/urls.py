from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.apps.posts.views',
	# Endpoint
	(r'create/?$', 'createPost'),
	(r'view/(?P<postId>\d+)/?$', 'viewPost'),
	(r'delete/(?P<postId>\d+)/?$', 'deletePost'),

)
