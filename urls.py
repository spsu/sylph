from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),

	# Frontend
	#(r'^/?$', 'sylph.system.frontend.views.index'),
	#(r'main/', include('sylph.system.frontend.urls')),

	# Endpoint
	(r'^endpoint/', include('sylph.core.endpoint.urls')),

	# Posts
	(r'^posts/', include('sylph.apps.posts.urls')),

	# Maintenance
	(r'reset/?$', 'sylph.core.backend.views.resetDb'), # Reset the DB
	#(r'populate/?$', 'sylph.core.backend.views.populateDb'), # Populate the DB
)
