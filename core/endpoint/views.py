# Endpoint Views
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response


def addNode(request):
	"""This view is responsible for adding a new node to the system."""
	# TODO: Try Celery to asynch request/poll the node. 

	def handleAddNode(request):
		print request.POST

	# TODO: POST HANDLE
	if request.method == 'POST':
		handleAddNode(request)
	else:
		if not True:
			raise Http404
			response = HttpResponse
			response['Cache-Control'] = 'no-cache'


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


