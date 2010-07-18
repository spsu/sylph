from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.apps.media.views',
	# Files
	('^$', 'file_index'),
	#('file/(?P<id>\d+)/', 'view_file'),

	# Images
	('^image/$', 'image_index'),
	('^image/view/(?P<id>\d+)/$', 'image_view'),
	#('image/(?P<id>\d+)/delete/', 'delete_image'),


)
