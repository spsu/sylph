from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.core.node.views',
	# Node management
	(r'^$', 'index'),
	(r'add/$', 'add_node'),
	(r'edit/$', 'edit_own_node'),
	(r'edit/(?P<node_id>\d+)/$', 'edit_other_node'),
	(r'view/(?P<node_id>\d+)/$', 'view_node'),
	(r'delete/(?P<node_id>\d+)/$', 'delete_node'),

	# Ajax urls
	(r'ajax_get_info/$', 'ajax_get_info'),
)

