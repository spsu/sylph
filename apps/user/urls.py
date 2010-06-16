from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.apps.user.views',
	# User pages
	(r'^/?$', 'index'),
	(r'^edit/$', 'edit_own_profile'),
	(r'^view/(?P<user_id>\d+)/$', 'view_profile'),
	(r'^delete/(?P<user_id>\d+)/$', 'delete_user'),

	# Ajax queries
	(r'ajax_edit/$', 'ajax_edit'),
	(r'ajax_info/$', 'ajax_info'),
)

