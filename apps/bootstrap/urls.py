from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.apps.bootstrap.views',
	(r'^$', 'index'),
	(r'add/$', 'add_site'),
	(r'delete/(?P<site_id>\d+)/$', 'delete_site'),
	(r'view/(?P<site_id>\d+)/$', 'view_site'),
	(r'edit/(?P<site_id>\d+)/$', 'edit_site'),
)

