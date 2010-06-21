from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Subscription

def list_all(request):
	"""Just show a list of all subscriptions"""
	ours = None
	theirs = None
	try:
		ours = Subscription.objects.filter(is_ours=True)
		theirs = Subscription.objects.filter(is_ours=False)
	except:
		pass

	return render_to_response('core/subscription/list.html', {
									'ours': ours,
									'theirs': theirs,
								},
								context_instance=RequestContext(request))

