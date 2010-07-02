from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.core.resource.views',
	# Resource overview
	(r'^$', 'resource_index'),
	(r'add/(?P<res_id>\d+)/$', 'resource_view'),
)

