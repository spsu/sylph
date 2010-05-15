from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),

	# Frontend
	(r'^/?$', sylph.frontend.views.index),
	(r'main/', include(sylph.frontend.urls)),

	# Endpoint
	(r'^endpoint/', include(sylph.endpoint.urls)),
)
