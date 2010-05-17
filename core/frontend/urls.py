from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^view/', sylph.frontend.views.view_item),
	(r'^post/', sylph.frontend.views.post_item),
	(r'^respond/', sylph.frontend.views.respond_item),

)
