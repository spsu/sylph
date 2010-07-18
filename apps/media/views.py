from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from models import *

def view_image(request, id):
	try:
		image = Image.objects.get(pk=id)
	except Image.DoesNotExist:
		return Http404

	return render_to_response('apps/media/view_image.html',
								{'image': image})


