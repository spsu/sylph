# "Frontend" Views
# Whatever that means in terms of short-term architecture...

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from sylph.core.resource.models import Resource
from sylph.core.backend.utils.database import sync_empty_database
from sylph.utils.markdown2 import markdown

def index(request):
	"""Index view for Sylph. Not much here"""

	# This is a lame attempt at catching an empty database. 
	sync_empty_database()

	readme = None
	todo = None

	try:
		fh = open('README.mkd')
		readme = fh.read()
		fh.close()
		readme = markdown(readme)
	except:
		pass

	try:
		fh = open('TODO.mkd')
		todo = fh.read()
		fh.close()
		todo = markdown(todo)
	except:
		pass

	return render_to_response('index.html', {
								'readme': readme,
								'todo': todo,
							  },
							  context_instance=RequestContext(request))

def viewThread():
	pass

def postNew():
	pass

def reply():
	pass


