from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

import sylph.test
from sylph.core.endpoint.models import Resource

from utilities import reset_database, sync_empty_database
from UserAccount import UserAccount

def index(request):
	"""Just supply a list of tasks."""

	# This is a lame attempt at catching an empty database. 
	sync_empty_database()

	return render_to_response('core/backend/index.html',
							  context_instance=RequestContext(request))
def test(request):
	"""A view to test code. Simplifies testing process."""
	return sylph.test.test(request)

# /system/reset
#@login_required
def reset(request):
	"""This method resets the entire database. Everything is dropped and
	rebuilt."""

	if request.method == 'POST':
		reset_database()
		return HttpResponseRedirect('/')

	return render_to_response('core/backend/reset-database.html',
							  context_instance=RequestContext(request))

# /system/signup
# TODO: Rename: /system/install
def signup(request):
	"""Signup for this sylph node."""
	acc = UserAccount()

	# Don't allow sign up again!
	if acc.exists():
		return HttpResponseRedirect('/') 
		
	class CreateAccountForm(forms.Form):
		"""Form for creating user account"""
		username = forms.CharField(max_length=30)
		password = forms.CharField(
						max_length=30,
						label=(u'Password'),
						widget=forms.PasswordInput(render_value=False))
		email = forms.EmailField(max_length=30)

	if request.method == 'POST':
		form = CreateAccountForm(request.POST)
		if form.is_valid():
			acc.create(form.cleaned_data['username'], 
					   form.cleaned_data['password'], 
					   form.cleaned_data['email'])

			# TODO: Login here! 
			return HttpResponseRedirect('/') # ACCOUNT CREATED!

		return render_to_response('core/backend/create-account.html',
								 	{'form': form},
									context_instance=RequestContext(request))

	else:
		form = CreateAccountForm()
		return render_to_response('core/backend/create-account.html',
								 	{'form': form},
									context_instance=RequestContext(request))

# /system/login
def loginView(request):
	return HttpResponse('test')

def logoutView(request):
	logout(request)
	return HttpResponseRedirect('/')
	
