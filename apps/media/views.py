from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import *

def file_index(request):
	"""Generate an index of all files."""
	files = []
	try:
		files = File.objects.all()
	except File.DoesNotExist:
		pass

	return render_to_response('apps/media/file_index.html', {'files':files},
						context_instance=RequestContext(request))

def image_index(request):
	"""Generate an index of all files."""
	images = []
	try:
		images = Image.objects.all()
	except File.DoesNotExist:
		pass

	return render_to_response('apps/media/image_index.html', {'images':images},
						context_instance=RequestContext(request))


def image_view(request, id):
	try:
		image = Image.objects.get(pk=id)
	except Image.DoesNotExist:
		return Http404

	return render_to_response('apps/media/image_view.html',
								{'image': image},
						context_instance=RequestContext(request))


