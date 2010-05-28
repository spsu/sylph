from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from sylph.core.backend.utils.install_state import is_installed

"""
The URLs for Sylph will only be defined if the installation process has been
followed by the user.

In the future it is important to consider how new modules will be installed. 
A database-driven URL system may need to replace Django's URL dispatcher. 
"""

urlpatterns = None

if not is_installed():

	urlpatterns = patterns('',
		(r'^/?$', 'sylph.core.backend.views.install_main'),
		(r'^reset/$', 'sylph.core.backend.views.install_reset'),
	) 

else:

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


# Static media serving happens regardless (THIS IS ONLY FOR DEVELOPMENT!)
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$',
			'django.views.static.serve', 
			{'document_root': settings.MEDIA_ROOT}),
	)

