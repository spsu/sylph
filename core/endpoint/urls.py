from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.core.endpoint.views',
	# Endpoint
	(r'viewnodes', 'viewNodes'),
)
