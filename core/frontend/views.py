# "Frontend" Views
# Whatever that means in terms of short-term architecture...
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response

# XXX: This is just prototyping...

def index(request):
	# TODO: Perhaps make this report a TODO list!
	return render_to_response('index.html')

def viewThread():
	pass

def postNew():
	pass

def reply():
	pass


