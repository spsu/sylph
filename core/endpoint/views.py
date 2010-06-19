from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from sylph.core.endpoint.exceptions import ProtocolErrorException

import datetime

# ================ ENDPOINT INDEX =========================

def index(request):
	"""All endpoint-related communications will be through this one 
	view, which will serve to dispatch to the appropriate handler."""

	# TODO: Make endpoint dispatcher here.
	# TODO: Will need endpoint dispatching library

	# * urls.py -> (dispatch to) -> views.py
	# * tasks.py
	# * keys.py -> (dispatch to) -> api.py
		# TODO: how is this affected by diff between push/pull? 


	# TODO: For the dispatcher, consider using a similar version of what Django
	# does. Check its internals. 

	# TODO: Non-keyed dispatch based on analysis of incoming payload. 
	# TODO: analyze diff between push/pull on both ends. 


	"""
	Dispatch Key, eg. 

		* send_profile
		* send_post
		* send_reply
		* request_profile
		etc
	

	1. Edit profile locally
	2. Signal task via celery to tell friends (or subscribers)
	3. Job does work
		state = { pending | error | recieved }

	Is django dispatch appropriate?

	
	"""

	# TODO: Dispatch key needs to be embedded in RDF request... I think.
	if not request.POST or 'dispatch' not in request.POST:
		print "No dispatch postdata!"
		raise ProtocolErrorException, "No dispatch postdata!" # TODO

	dispatch = request.POST['dispatch']

	# TODO: I need to write an actual dispatcher!!!

	# ======== Node Disptaching ===========================

	print "Attempting to dispatch: %s" %dispatch # TODO DEBUG

	if dispatch in ['ping', 'node_ping']:
		from sylph.core.node.api import ping_response
		return ping_response(request)

	if dispatch == 'node_add':
		from sylph.core.node.api import add
		return add(request)

	if dispatch == 'node_delete':
		from sylph.core.node.api import delete
		return delete(request)

	# ======== User Dispatching ===========================

	if dispatch == 'user_update': # TODO
		"""Simply ask for the user's profile, updates, etc."""
		from sylph.apps.user.api import get_profile
		return get_profile(request)

	if dispatch == 'user_push':
		from sylph.apps.user.api import update_profile
		return update_profile(request)

	if dispatch == 'user_get': # TODO
		"""Get a user profile from the user's URI."""
		from sylph.apps.user.api import get
		return get(request)

	if dispatch == 'user_get_by_node': # TODO
		"""Look up a user for a node URI."""
		from sylph.core.user.api import get_by_node
		return get_by_node(request)

	return HttpResponse('TODO')


