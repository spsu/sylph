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
	# TODO: For now, index is just a list of nodes. 
	#		In the future, make this a status feed or similar.
	return listNodes(request)


# ================ LIST NODES ===================

def listNodes(request):
	"""A list of all the nodes in the system."""

	nodes = Node.objects.all()
	return render_to_response('apps/node/list.html',
							{'nodes': nodes },
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


# ================ VIEW NODE ====================

def viewNode(request, nodeId):
	return render_to_response('apps/node/view.html',
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


# ================ ADD NODE =====================

@login_required
def addNode(request):

	class NewNodeForm(ModelForm):
		"""Form for creating posts"""
		class Meta:
			model = Node
			fields = ['url']

	if request.method == 'POST':
		form = NewNodeForm(request.POST)
		if form.is_valid():
			node = form.save(commit=False)

			node.name = ''
			node.node_type = 'X'
			node.is_to_resolve = True
			node.status = 'U'

			node.datetime_added = datetime.datetime

			node.save()

			return HttpResponseRedirect('/node/')

		return render_to_response('apps/node/add.html',
								 	{'form': form}, 
									context_instance=RequestContext(request))

	else:
		form = NewNodeForm()
		return render_to_response('apps/node/add.html',
								 	{'form': form}, 
									context_instance=RequestContext(request))


# ================ REMOVE NODE ==================

@login_required
def removeNode(request, nodeId):
	return render_to_response('apps/node/remove.html',
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


# ================ MANAGE NODE ==================

@login_required
def manageNode(request, nodeId):
	return render_to_response('apps/node/manage.html',
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')



