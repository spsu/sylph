from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext

from models import ProfilePost
from sylph.apps.user.models import User
from sylph.utils.uri import generate_uuid

from datetime import datetime

def profile_post_index(request, user_id):
	"""Show all the profile posts for a user."""
	try:
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		raise Http404

	posts = []
	try:
		posts = ProfilePost.objects.filter(for_user=user) \
									.order_by('-datetime_created')
	except:
		pass

	return render_to_response('apps/social/profile_post/index.html', {
									'user': user,
									'posts': posts,
								},
								context_instance=RequestContext(request))


def profile_post_view(request, post_id):
	"""View a single profile post (Not very useful...)"""
	try:
		post = ProfilePost.objects.get(pk=post_id)
	except ProfilePost.DoesNotExist:
		raise Http404

	user = None
	try:
		user = post.for_user
		#user = User.objects.get(post.for_user)
	except:
		pass

	return render_to_response('apps/social/profile_post/view.html', {
									'user': user,
									'post': post,
								},
								context_instance=RequestContext(request))


def profile_post_create(request, user_id):
	"""Create a new profile post on a given user."""
	try:
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		raise Http404

	class NewProfilePostForm(forms.ModelForm):
		"""Form for creating a new profile post."""
		class Meta:
			model = ProfilePost
			fields = [
				'contents',
			]

	if request.method == 'POST':
		form = NewProfilePostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.uri = generate_uuid()
			post.for_user = user
			post.author = User.objects.get(pk=1)
			post.datetime_created = datetime.today()
			post.save()

			return HttpResponseRedirect('/user/view/%d/'%user.pk)

	else:
		form = NewProfilePostForm()

	return render_to_response('apps/social/profile_post/create.html', {
									'form': form,
								},
								context_instance=RequestContext(request))

def profile_post_delete(request, post_id):
	pass

def profile_post_edit(request, post_id):
	pass


