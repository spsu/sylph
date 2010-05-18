from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),

	# Frontend
	(r'^/?$', 'sylph.core.frontend.views.index'),
	#(r'main/', include('sylph.system.frontend.urls')),

	# Applications the user can use
	(r'^posts/', include('sylph.apps.posts.urls')),
	(r'^nodes/', include('sylph.apps.nodes.urls')), # User-accessible management
	(r'^social/', include('sylph.apps.social.urls')),

	# Endpoint - NOT FOR USERS.
	(r'^endpoint/', include('sylph.core.endpoint.urls')),

	# Maintenance
	(r'reset/?$', 'sylph.core.backend.views.resetDb'), # Reset the DB
	#(r'populate/?$', 'sylph.core.backend.views.populateDb'), # Populate the DB
)
