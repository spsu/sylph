from django.conf import settings

from sylph.core.backend.utils.install_state import is_installed
from sylph.apps.user.models import User


def ip_address(request):
	"""Return IP address (from Django docs)"""
	return {'ip_address': request.META['REMOTE_ADDR']}

def inject_settings(request):
	"""Allows use of Django settings in templates""" # XXX: is this wise?
	return {'settings': settings}

def owner_user_ref(request):
	"""
	Assuming the system has been set up, make the owner's account
	always referenceable in the templates. (TODO: Fix query redundancy)
	"""
	if not is_installed():
		return {}

	# If the user model is changed, reset form becomes inaccessible
	if request.META['PATH_INFO'].startswith('/reset'):
		return {}

	try:
		user = User.objects.get(pk=settings.OUR_USER_PK)
	except User.DoesNotExist:
		return {} # TODO: Is it wise to surpress this?

	return {'owner': user}

# TODO: Context processor for mail messages, etc. (And ajax update)

