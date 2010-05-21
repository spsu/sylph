from django.conf.urls.defaults import *

urlpatterns = patterns('sylph.core.backend.views',
	# Just a list of tasks
	(r'^/?$', 'index'),
 
	# User Functions
	(r'signup/?$', 'signup'),
	(r'logout/?$', 'logoutView'),

	# Management Functions
	(r'reset/?$', 'reset'),
	#(r'populate/?$', 'populateDb'), # Populate the DB with test/dummy data

	# Test 
	(r'test/?$', 'test'),
)

# Use builtin login system
urlpatterns += patterns('',
	(r'login/?$', 'django.contrib.auth.views.login', 
				  {'template_name': 'core/backend/login.html'}),
)
