from django.db import models

# TODO: Figure out how to limit to one instance. 
class SystemUser(models.Model):
	pass
	#username
	#passhash

	# XXX: Or wait, couldn't I just extend from Django's Auth system?
