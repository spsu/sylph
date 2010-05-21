from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.core.endpoint.views',
	# List and view
	(r'^/$', 'index'), # Activity stream

	# TODO: Categorize into user/macine nodes.
	# TODO: Will need pagination, etc.
	(r'list/$', 'listNodes'), # List of nodes. 

	(r'view/(?P<nodeId>\d+)/$', 'viewNode'),

	# Management
	(r'add/?$', 'addNode'), # TODO: Make an API for users external of the Django app!
	(r'remove/(?P<nodeId>\d+)/$', 'removeNode'),
	(r'manage/(?P<nodeId>\d+)/$', 'manageNode'), # Permissions, etc.
)
