from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from sylph.core.backend.utils.install_state import is_installed

# Note: This file is only interpreted once: at webserver startup!

#admin.autodiscover()

urlpatterns = patterns('',
	#(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	#(r'^admin/', include(admin.site.urls)),

	# Specific views
	(r'^/?$', 'sylph.core.backend.views.index'),
	(r'^reset/$', 'sylph.core.backend.views.reset'),
	(r'^endpoint/$', 'sylph.core.endpoint.views.index'),
	(r'^cron(job)?s?/$', 'sylph.core.backend.views.run_jobs'), # An alias

	# Application level
	(r'^bootstrap/', include('sylph.apps.bootstrap.urls')),	# bootstrap -> www?
	(r'^post/', include('sylph.apps.post.urls')),
	(r'^user/', include('sylph.apps.user.urls')),
	(r'^social/', include('sylph.apps.social.urls')),
	(r'^blog/', include('sylph.apps.blog.urls')),

	# System Level
	(r'^node/', include('sylph.core.node.urls')),
	(r'^jobs/', include('sylph.core.jobs.urls')),
	(r'^system/', include('sylph.core.backend.urls')), # Manage the system
	(r'^sylph/', include('sylph.core.backend.urls')), # Manage the system
	(r'^subscription/', include('sylph.core.subscription.urls')),
	(r'^resource/', include('sylph.core.resource.urls')),
	#(r'main/', include('sylph.system.frontend.urls')),
)

# Static media serving (THIS IS ONLY FOR DEVELOPMENT SERVERS!)
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
			'django.views.static.serve',
			{'document_root': settings.MEDIA_ROOT}),
	)

