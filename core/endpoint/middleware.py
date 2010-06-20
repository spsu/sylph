from django.conf import settings
from django.http import HttpResponse

class EndpointExceptionHandlerMiddleware(object):
	"""
	Runs whenever an exception occurs in endpoint mode.
	This will be used to easily diagnose problems in debug mode,
	and later to return better error messages (in RDF).
	"""

	def __init__(self):
		# If used, be aware that init only runs once, at the webserver start!
		pass

	def process_exception(self, request, exception):
		"""Process the exception.
		This runs for ALL pages, but we need to ensure we only run it
		for the endpoint urls."""
		print "process_exception: %s" % str(exception) # TODO: DEBUG
		path = request.META['PATH_INFO']
		print path

		if not path.startswith(settings.ENDPOINT_URI):
			return None

		typ = str(type(exception))
		typ = typ.replace('<', '[').replace('>', ']')
		ret = "Exception %s : %s" % (typ, str(exception))
		return HttpResponse(ret)

