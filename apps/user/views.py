from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import *
from sylph.apps.social.models import ProfilePost
import tasks

from datetime import datetime
import hashlib


# ============ Social Index ===============================

def index(request):
	users = User.objects.all()
	return render_to_response('apps/user/index.html', {
									'users': users,
							},
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')

# ============ Add Person Form ============================

def add_person_form(request):
	"""
	(TODO)

	We should have a _single_ text entry where the following can be
	added:
		* OpenID (the page will contain metadata to an endpoint)
		* SylphID (similar to OpenID, but is the person's Resource URI)
		* Endpoint URI, and we query the endpoint for owner data
		* email address (and we query a directory service and possibly friends)

	This makes it _incredibly_ easy to add a person. If more search capability
	is required, then we can search a directory w/ info such as phone number,
	previous school, company, etc.

	I suppose this makes us "follow" the person...

	Keep this a separate view from simply adding a friend of a friend.
	"""
	pass

# ============ Edit Profile ===============================

def edit_own_profile(request):
	user = None
	try:
		user = User.objects.get(pk=settings.OUR_USER_PK)
	except User.DoesNotExist:
		raise Http404 # TODO: This is actually a core system failure!

	class EditProfileForm(forms.ModelForm):
		"""Form for editing one's profile"""
		class Meta:
			model = User
			fields = [
						'username',
						'first_name',
						'middle_name',
						'last_name',
						'title',
						'bio'
					]

	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=user)
		if form.is_valid():
			u = form.save(commit=False)
			u.datetime_edited = datetime.today()
			u.save() # Save calls signal handler for push_profile.

			#tasks.push_profile.delay()
			return HttpResponseRedirect('/user/view/1/')

	else:
		form = EditProfileForm(instance=user)

	return render_to_response('apps/user/edit_profile.html',
								{'form': form},
								context_instance=RequestContext(request))

# ============ View Profile ===============================

def view_profile(request, user_id):
	"""View a profile by user id"""
	profile = None
	try:
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		raise Http404

	posts = []
	try:
		posts = ProfilePost.objects.filter(for_user=user) \
									.order_by('-datetime_created')
	except ProfilePost.DoesNotExist:
		pass

	return render_to_response('apps/user/view_profile.html', {
									'user': user,
									'posts': posts,
							},
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')

# ============ Ajax editing ===============================

def ajax_edit(request):
	"""Edit the profile with ajax."""
	if not request.is_ajax() or request.method != 'POST':
		raise Exception, "Must be ajax post!"

	if 'id' not in request.POST:
		raise Exception, "No id!" # TODO: Error logging

	try:
		user = User.objects.get(pk=settings.OUR_USER_PK)
	except User.DoesNotExist:
		raise Exception, "Main user does not exist!!" # TODO: System err

	user.datetime_edited = datetime.today()

	if request.POST['id'] == 'bio':
		user.bio = request.POST['value']
		user.save()
		return HttpResponse(user.bio_with_markup())

	if request.POST['id'] == 'name':
		user.set_name(request.POST['value']) # TODO: Not sanitized!
		user.save()
		return HttpResponse(user.get_name())

	if request.POST['id'] == 'username':
		user.username = request.POST['value'] # TODO: Not sanitized!
		user.save()
		return HttpResponse(user.get_username())

	raise Exception, "Unknown request..."

def ajax_info(request):
	"""Load ajax info on the user profile."""

	try:
		user = User.objects.get(pk=settings.OUR_USER_PK)
	except User.DoesNotExist:
		raise Exception, "Main user does not exist!!" # TODO: System err
		# TODO: Ajax error

	print request.POST
	return HttpResponse(user.bio)

