from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.core.resource.views',
	# Resource overview
	(r'^$', 'resource_index'),
	(r'view/(?P<res_id>\d+)/$', 'resource_view'),
	(r'redirect/(?P<res_type>\w+)/(?P<res_id>\d+)/$', 'resource_redirect'),
)

