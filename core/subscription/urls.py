from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.core.subscription.views',
		(r'^$', 'list_all'),
		#(),
)
