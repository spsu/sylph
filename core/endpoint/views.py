# Endpoint Views
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response


def addNode(request):

	# TODO: POST HANDLE

	if not True:
		raise Http404

	return render_to_response('core/endpoint/add-node.html')


def viewNodes(request):
	nodes = []
	return render_to_response('core/endpoint/view-nodes.html', {
									'nodes':	nodes,
							},
							mimetype='application/xhtml+xml')

def removeNode(request):
	# TODO: POST HANDLE
	pass


