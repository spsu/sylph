from sylph.core.backend.utils.install_state import is_installed
from sylph.core.backend.views import install_main

from django.conf import settings
from django.http import HttpResponseRedirect

class EnsureInstalledMiddleware(object):
	"""
	Middleware to ensure that the Sylph portal has been installed 
	properly, and if not, run an installation view.
	"""

	def __init__(self):
		# If used, be aware that init only runs once, at the webserver start!
		pass

	def process_view(self, request, view_func, view_args, view_kwargs):
		"""Runs just prior to having the view dispatched to and checks
		if the user exists in the database."""
		if is_installed():
			return None

		path = request.META['PATH_INFO']

		if path.startswith(settings.MEDIA_URL):
			return None

		# TODO: Not very configurable...
		if path not in ['', '/', '/reset', '/reset/']:
			return HttpResponseRedirect('/')

		if path.startswith('/reset'):
			return False

		# Call installation view instead!
		return install_main(request)

