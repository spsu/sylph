from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.apps.blog.views',
	# Blog Items
	(r'^$', 'blogitem_index'),
	(r'^create/$', 'blogitem_create'),
	(r'^view/(?P<item_id>\d+)/$', 'blogitem_view'),
	(r'^edit/(?P<item_id>\d+)/$', 'blogitem_edit'),
	(r'^delete/(?P<item_id>\d+)/$', 'blogitem_delete'),

	# Blog Subscriptions
	(r'^subscription/$', 'subscription_index'),
	(r'^subscription/view/(?P<subs_id>\d+)/$', 'subscription_view'),
	(r'^subscription/add/$', 'subscription_add'),
	(r'^subscription/edit/(?P<subs_id>\d+)/$', 'subscription_edit'),
	(r'^subscription/delete/(?P<subs_id>\d+)/$', 'subscription_delete'),
)

