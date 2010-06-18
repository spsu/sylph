from django.db.models import Model
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext

from sylph.core.endpoint.exceptions import ProtocolErrorException
from sylph.utils.data.RdfSerializer import RdfSerializer

from sylph.apps.user.models import User
from sylph.core.node.models import Node

from models import *

from datetime import datetime

def list_subscriptions_offered(request):
	"""Another node is asking us which subscriptions we offer."""
	pass # TODO

	"""
	Possible list of subscriptions:

		* user -> profile changes
		* social? -> wall posts made by user
		* social? -> wall posts made by others to user
		* blog -> blog items made by user
		* blog -> blog edits made by user (TODO: in future cache edits??)
		* blog -> post responses made by user
		* bootstrap -> ???? (How is this even going to work?)
	"""

def subscribe_to(request)
	"""Another node is asking to subscribe to something."""
	accept = False

	# * is this a valid type of subscription?

	# * do we accept? (will involve app-specific rules.)
	if not accept:
		return HttpResponse('rejected') # TODO response

	# TODO: Make sure we use the right subscription subclass!
	subs = Subscription()
	subs.node = node
	subs.is_ours = False
	subs.datetime_created = datetime.now()
	subs.save()

	return HttpResponse('accepted') # TODO response, also return params!

