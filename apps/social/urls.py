from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.apps.social.views',

	(r'^/?$', 'index_view'),
	(r'^edit/$', 'edit_own_profile'),
	(r'^view/(?P<user_id>\d+)/$', 'view_profile'),
	(r'^delete/(?P<user_id>\d+)/$', 'delete_user'),

)
