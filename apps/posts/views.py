# Post Views

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django import forms
from models import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from datetime import datetime
import hashlib

# ============ Post Index (Parentless) ==========

def indexParentless(request):
	posts = Post.objects.filter(reply_to_root__isnull = True)
	return render_to_response('apps/posts/index.html', {
									'posts':	posts,
							}, 
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


# ============ Post Index (All) =================

def indexAll(request):
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

	class NewPostForm(forms.ModelForm):
		"""Form for creating posts"""
		class Meta:
			model = Post
			fields = ['title', 'contents']

	if request.method == 'POST':
		form = NewPostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.datetime_created = datetime.today()
			# FIXME TEMP URL
			post.url = 'http://temp/post/' + \
						hashlib.md5(str(datetime.today())).hexdigest() 
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
	posts = []
	try:
		posts = Post.objects.filter(Q(pk=postId) | Q(reply_to_root=postId))
	except Post.DoesNotExist:
		raise Http404

	print posts

	return render_to_response('apps/posts/view.html', {
									'posts': posts,
							}, 
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


# ============ Reply Post =======================

def replyPost(request, postId):
	"""Reply to a post"""
	parent = None
	try:
		parent = Post.objects.get(pk=postId)
	except Post.DoesNotExist:
		raise Http404

	class NewReplyForm(forms.ModelForm):
		"""Form for creating replies"""
		reply_to_root = forms.IntegerField(
							widget=forms.widgets.HiddenInput(),
							initial = parent.id)

		reply_to_parent = forms.IntegerField(
							widget=forms.widgets.HiddenInput(),
							initial = parent.id)

		class Meta:
			model = Post
			fields = ['contents']

	if request.method == 'POST':
		form = NewReplyForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.datetime_created = datetime.today()
			post.title = "Re: " + parent.title
			# FIXME TEMP URL
			post.reply_to_root = parent
			post.url = 'http://temp/post/' + \
						hashlib.md5(str(datetime.today())).hexdigest() 
			post.save()
			return HttpResponseRedirect('/posts/')

		return render_to_response('apps/posts/reply.html',
								 	{'form': form}, 
									context_instance=RequestContext(request))

	else:
		form = NewReplyForm()
		return render_to_response('apps/posts/reply.html',
								 	{'form': form}, 
									context_instance=RequestContext(request))


# ============ Delete Post ======================

def deletePost(request, postId):
	# TODO: POST HANDLE
	pass


