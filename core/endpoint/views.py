# Node Views

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.forms import ModelForm
from models import *
from django.template import RequestContext

import datetime
from models import Node

# ================ INDEX ========================

def index(request):
	"""All endpoint-related communications will be through this one 
	view, which will serve to dispatch to the appropriate handler."""

	# TODO
	pass


