from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import *
from sylph.apps.user.models import User
from sylph.utils.uri import generate_uuid

from datetime import datetime
import hashlib

# ============ Post Index (Parentless) ==========

def index_parentless(request):
	posts = Post.objects.filter(reply_to_root__isnull=True)
	return render_to_response('apps/post/index.html', {
									'posts': posts,
							  }, 
							  context_instance=RequestContext(request),
							  mimetype='application/xhtml+xml')


# ============ Post Index (All) =================

def index_all(request):
	posts = Post.objects.all()
	return render_to_response('apps/post/index.html', {
									'posts': posts,
							  }, 
							  context_instance=RequestContext(request),
							  mimetype='application/xhtml+xml')


# ============ View Post ========================

def view_post(request, post_id):
	"""View a post by its id"""
	posts = []
	try:
		posts = Post.objects.filter(Q(pk=post_id) | Q(reply_to_root=post_id))
	except Post.DoesNotExist:
		raise Http404

	print posts

	return render_to_response('apps/post/view.html', {
									'posts': posts,
							  },
							  context_instance=RequestContext(request),
							  mimetype='application/xhtml+xml')


# ============ Create Post ======================

#@login_required
def create_post(request):
	"""Create a new post."""

	class NewPostForm(forms.ModelForm):
		"""Form for creating posts"""
		class Meta:
			model = Post
			fields = ['title', 'contents']

	form = None
	if request.method == 'POST':
		form = NewPostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.datetime_created = datetime.today()
			# FIXME TEMP URL
			post.uri = 'http://temp/post/' + \
						hashlib.md5(str(datetime.today())).hexdigest()

			user = User.objects.get(pk=settings.OUR_USER_PK)
			post.author = user

			post.save()
			return HttpResponseRedirect('/post/')

	else:
		form = NewPostForm()

	return render_to_response('apps/post/create.html', {
									'form': form
								},
								context_instance=RequestContext(request))

# ============ Reply Post =======================

def reply_post(request, post_id):
	"""Reply to a post"""
	parent = None
	try:
		parent = Post.objects.get(pk=post_id)
	except Post.DoesNotExist:
		raise Http404

	class NewReplyForm(forms.ModelForm):
		"""Form for creating replies"""
		reply_to_root = forms.IntegerField(
							widget=forms.widgets.HiddenInput(),
							initial = parent.pk)

		reply_to_parent = forms.IntegerField(
							widget=forms.widgets.HiddenInput(),
							initial = parent.pk)

		class Meta:
			model = Post
			fields = ['contents']

	form = None
	if request.method == 'POST':
		form = NewReplyForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.datetime_created = datetime.today()
			post.title = "Re: " + parent.title
			post.reply_to_root = parent
			post.uri = generate_uuid() # FIXME: TEMP URL
			user = User.objects.get(pk=settings.OUR_USER_PK)
			post.author = user

			post.save()
			return HttpResponseRedirect('/post/')

	else:
		form = NewReplyForm()

	return render_to_response('apps/post/reply.html', {
									'form': form
								},
								context_instance=RequestContext(request))


# ============ Edit Post ======================

def edit_post(request, post_id):
	# TODO: POST HANDLE
	pass

# ============ Delete Post ======================

def delete_post(request, post_id):
	# TODO: POST HANDLE
	pass

