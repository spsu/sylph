from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.core.backend.views',
	# Just a list of tasks
	(r'^/?$', 'index'),
 
	# User Functions
	(r'signup/?$', 'signup'),
	(r'login/?$', 'loginView'),
	(r'logout/?$', 'logoutView'),

	# Management Functions
	(r'reset/?$', 'reset'),
	#(r'populate/?$', 'populateDb'), # Populate the DB with test/dummy data
)
