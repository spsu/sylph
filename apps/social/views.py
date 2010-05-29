# Social Views

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from models import *

from datetime import datetime
import hashlib


# ============ Social Index ===============================

def index(request):
	users = User.objects.all()
	return render_to_response('apps/social/index.html', {
									'users': users,
							}, 
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


# ============ Edit Profile ===============================

def edit_own_profile(request):
	user = None
	try:
		user = User.objects.get(pk=1)
	except User.DoesNotExist:
		raise Http404 # TODO: This is actually a core system failure!

	class EditProfileForm(forms.ModelForm):
		"""Form for editing one's profile"""
		class Meta:
			model = User
			fields = ['username', 'first_name', 'middle_name', 'last_name',
					  'title', 'bio']

	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=user)
		if form.is_valid():
			u = form.save(commit=False)
			u.datetime_edited = datetime.today()
			u.save()
			return HttpResponseRedirect('/profile/view/1/')

	else:
		form = EditProfileForm(instance=user)

	return render_to_response('apps/social/edit_profile.html',
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

	return render_to_response('apps/social/view_profile.html', {
									'user': user,
							}, 
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


