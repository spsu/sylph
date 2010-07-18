from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.apps.media.views',
	#('/', 'index'),
	#('file/(?P<id>\d+)/', 'view_file'),

	# Images
	('image/view/(?P<id>\d+)/', 'view_image'),
	#('image/(?P<id>\d+)/delete/', 'delete_image'),


)
