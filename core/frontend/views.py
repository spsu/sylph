# "Frontend" Views
# Whatever that means in terms of short-term architecture...

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from sylph.core.resource.models import Resource
from sylph.core.backend.utils.database import sync_empty_database

def index(request):
	"""Index view for Sylph. Not much here"""

	# This is a lame attempt at catching an empty database. 
	sync_empty_database()

	return render_to_response('index.html', 
							  context_instance=RequestContext(request))

def viewThread():
	pass

def postNew():
	pass

def reply():
	pass


