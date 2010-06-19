from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.apps.social.views',

	# Social networking
	(r'add/$', 'add_person'), # XXX: Not good/actual URIs.
	(r'remove/$', 'remove_person'),

	# Profile posts
	(r'post/index/(?P<user_id>\d+)/$', 'profile_post_index'),
	(r'post/create/(?P<user_id>\d+)/$', 'profile_post_create'),
	(r'post/view/(?P<post_id>\d+)/$', 'profile_post_view'),
	(r'post/delete/(?P<post_id>\d+)/$', 'profile_post_delete'),
	(r'post/edit/(?P<post_id>\d+)/$', 'profile_post_edit'),
)

