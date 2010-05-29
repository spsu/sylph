from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django import forms

import sylph.test

from sylph.core.endpoint.models import Resource
from sylph.apps.social.models import User

from utils.install_state import is_installed, INSTALLED
from utils.database import reset_database, sync_empty_database
from utils.Configs import Configs

from UserAccount import UserAccount
from sylph.utils.file import touch

import time

def index(request):
	"""Just supply a list of tasks."""

	# This is a lame attempt at catching an empty database. 
	sync_empty_database()

	return render_to_response('core/backend/index.html',
							  context_instance=RequestContext(request))
def test(request):
	"""A view to test code. Simplifies testing process."""
	return sylph.test.test(request)


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


# ============ Installation ===============================

def install_main(request):
	"""	This view constitutes the installer process for Sylph."""
	if is_installed():
		raise Exception, "Cannot reinstall software unless data is wiped."

	user = None
	try:
		user = User.objects.get(id=1)
	except:
		# TODO
		raise Exception, "TODO: resync-database!"
	
	# TODO: This should be broken down into a multi-step creation process
	class NewUserInstallForm(forms.Form):
		"""Form for creating user account"""
		#login_username = forms.CharField(max_length=30, required=True)
		public_username = forms.CharField(max_length=24, required=True)
		#password = forms.CharField(
		#				max_length=30,
		#				label=(u'Password'),
		#				widget=forms.PasswordInput(render_value=False),
		#				required=True)
		f_name = forms.CharField(max_length=30, required=False,
						label=(u'First name'))
		m_name = forms.CharField(max_length=30, required=False,
						label=(u'Middle name'))
		l_name = forms.CharField(max_length=30, required=False,
						label=(u'Last name'))
		email = forms.EmailField(max_length=30, required=False)

	form = None
	if request.method == 'POST':
		form = NewUserInstallForm(request.POST)

		if form.is_valid():
			data = form.cleaned_data

			user.username = data['public_username']
			user.first_name = data['f_name']
			user.middle_name = data['m_name']
			user.last_name = data['l_name']
			user.email = data['email']

			user.uri = 'http://TODO/username/' # TODO: Generate username URI

			user.save()

			# TODO: Create site login account

			configs = Configs()
			configs.installation_status = INSTALLED
			configs.save()

			# TODO: Login here! 
			return HttpResponseRedirect('/') # ACCOUNT CREATED!
		

	else:
		form = NewUserInstallForm(initial={'public_username': user.username})


	return render_to_response('core/backend/install/index.html',
							  {'form': form},
							  context_instance=RequestContext(request))


# ============ Reset Everything ===========================

def reset(request):	
	"""Reset everything, tear down and rebuild database, and begin the
	install process all over. Obviously this will need to be locked 
	down when the software is complete."""
	template = 'core/backend/install/reset.html'
	if is_installed():
		template = 'core/backend/reset-database.html'

	if request.method == 'POST':
		reset_database()
		return HttpResponseRedirect('/')

	return render_to_response(template,
							  context_instance=RequestContext(request))


# ============ Misc =======================================

# /system/login
def loginView(request):
	return HttpResponse('test')

def logoutView(request):
	logout(request)
	return HttpResponseRedirect('/')
	
