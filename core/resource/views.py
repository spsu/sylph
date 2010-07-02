from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import *

from datetime import datetime


# ============ Resouce Index ==============================

def resource_index(request):
	"""Show all resources, for debugging purposes"""
	resources = []
	try:
		resources = Resource.objects.all() \
									.order_by('pk')
	except Exception as e:
		pass
	return render_to_response('core/resource/index.html', {
									'resources': resources,
							},
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')

# ============ View Resource ==============================

def resource_view(request, res_id):
	"""View info on a resource, for debugging purposes"""
	try:
		resource = Resource.objects.get(pk=res_id)
	except Resource.DoesNotExist:
		raise Http404

	return render_to_response('core/resource/view.html', {
									'resource': resource,
							},
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')

