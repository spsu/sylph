# Node Views

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.forms import ModelForm
from models import *
from django.template import RequestContext

import datetime

# ================ INDEX ========================

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

	return HttpResponse('TODO')


