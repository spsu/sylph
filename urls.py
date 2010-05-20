from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),

	# Frontend
	(r'^/?$', 'sylph.core.frontend.views.index'),
	#(r'main/', include('sylph.system.frontend.urls')),

	# Application level
	(r'^posts/', include('sylph.apps.posts.urls')),
	#(r'^social/', include('sylph.apps.social.urls')),

	# System Level
	(r'^node/', include('sylph.core.endpoint.urls')),
	(r'^system/', include('sylph.core.backend.urls')), # Manage the system
)
