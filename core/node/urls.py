from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.core.node.views',
	# Endpoint
	(r'^$', 'index'),
	(r'add/$', 'add_node'),
	(r'edit/$', 'edit_own_node'),
	(r'view/(?P<node_id>\d+)/$', 'view_node'),
	(r'delete/(?P<node_id>\d+)/$', 'delete_node'),
)

