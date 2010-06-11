from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.apps.user.views',

	(r'^/?$', 'index'),
	(r'^edit/$', 'edit_own_profile'),
	(r'^view/(?P<user_id>\d+)/$', 'view_profile'),
	(r'^delete/(?P<user_id>\d+)/$', 'delete_user'),

)
