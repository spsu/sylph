from django.db import models

# TODO: Other models related to maintaining the backend, SUCH AS JOBS!
# (Or will celery be able to handle Jobs?)

# ============ Backend Config ===================

class BackendConfig(models.Model):
	"""Configuration options for the Sylph instance.
	Configurations can be used in a wide variety of circumstances."""

	# Key 
	key = models.CharField(max_length=30, blank=False, null=False)

	# Human-readable description of the config value.
	description = models.CharField(max_length=255, blank=True, null=False)

	# Datatype to handle as / cast to
	DATATYPES = (
		('B', 'Boolean'),
		('I', 'Integer'),
		('F', 'Float'),
		('S', 'String'),
		('H', 'String (with HTML)'),
		('P', 'Python'), # XXX: Be careful... 
	)
	datatype = models.CharField(max_length=1, choices=DATATYPES)

	# Value
	value = models.CharField(max_length=255, blank=True, null=False)

	# Large value (eg. serialized Python objects, etc.) Usually BLANK. 
	value_large = models.TextField(blank=True, null=False)

