# Post Views

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.forms import ModelForm
from models import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from datetime import datetime

# ============ Post Index =======================

def index(request):
	posts = Post.objects.all()
	return render_to_response('apps/posts/index.html', {
									'posts':	posts,
							}, 
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


# ============ Create Post ======================

#@login_required
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
			post = form.save(commit=False)
			post.datetime_created = datetime.today()
			post.save()
			return HttpResponseRedirect('/posts/')

		return render_to_response('apps/posts/create.html',
								 	{'form': form}, 
									context_instance=RequestContext(request))

	else:
		form = NewPostForm()
		return render_to_response('apps/posts/create.html',
								 	{'form': form}, 
									context_instance=RequestContext(request))


# ============ View Post ========================

def viewPost(request, postId):
	"""View a post by its id"""
	try:
		post = Post.objects.get(pk=postId)
	except Post.DoesNotExist:
		raise Http404

	return render_to_response('apps/posts/view.html', {
									'post':	post,
							}, 
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


# ============ Delete Post ======================

def deletePost(request, postId):
	# TODO: POST HANDLE
	pass


