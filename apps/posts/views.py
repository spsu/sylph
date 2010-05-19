# Post Views

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.forms import ModelForm
from models import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def createPost(request):
	"""Create a new post."""
	# TODO: Try Celery to asynch request/poll the node. 

	class NewPostForm(ModelForm):
		"""Form for creating posts"""
		class Meta:
			model = Post
			fields = ['title', 'contents']

	if request.method == 'POST':
		form = NewPostForm(request.POST)
		if form.is_valid():
			post = form.save()
			return HttpResponseRedirect('/posts/')

		return render_to_response('apps/posts/create-post.html',
								 	{'form': form}, 
									context_instance=RequestContext(request))

	else:
		form = NewPostForm()
		return render_to_response('apps/posts/create-post.html',
								 	{'form': form}, 
									context_instance=RequestContext(request))


def index(request):
	posts = Post.objects.all()
	return render_to_response('apps/posts/index.html', {
									'posts':	posts,
							}, 
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


def viewPost(request, postId):
	posts = Post.objects.all()

	return render_to_response('core/endpoint/view-nodes.html', {
									'posts':	posts,
							}, 
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


def deletePost(request, postId):
	# TODO: POST HANDLE
	pass


