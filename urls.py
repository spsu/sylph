from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),

	# Frontend
	(r'^/?$', 'sylph.core.frontend.views.index'),
	#(r'main/', include('sylph.system.frontend.urls')),

	# Application level
	(r'^post/', include('sylph.apps.post.urls')),
	#(r'^social/', include('sylph.apps.social.urls')),

	# System Level
	(r'^node/', include('sylph.core.endpoint.urls')),
	(r'^system/', include('sylph.core.backend.urls')), # Manage the system
)

# Static media serving (ONLY IN DEVELOPMENT!)
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$',
			'django.views.static.serve', 
			{'document_root': settings.MEDIA_ROOT}),
	)

