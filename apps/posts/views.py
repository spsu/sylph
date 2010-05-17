# Post Views

from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response

def createPost(request):
	"""Create a new post."""
	# TODO: Try Celery to asynch request/poll the node. 

	# TODO: POST HANDLE
	def handleCreatePost(request):
		print request.POST

	def todoCreatePost(request):
		return render_to_response('apps/posts/create-post.html')

	if request.method == 'POST':
		return handleCreatePost(request)
	else:
		return todoCreatePost(request)



def viewPost(request, postId):
	nodes = []




	return render_to_response('core/endpoint/view-nodes.html', {
									'nodes':	nodes,
							},
							mimetype='application/xhtml+xml')


def deletePost(request, postId):
	# TODO: POST HANDLE
	pass


