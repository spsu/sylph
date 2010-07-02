from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext

from sylph.core.resource.models import Resource
from sylph.core.node.models import Node
from sylph.apps.user.models import User

from utils.install_state import is_installed, INSTALLED
from utils.database import reset_database, sync_empty_database
from utils.Configs import Configs

from UserAccount import UserAccount

import time

# ============ Index View =================================

def index(request):
	"""Just supply a list of tasks."""

	# This is a lame attempt at catching an empty database. 
	sync_empty_database()

	return render_to_response('core/backend/index.html',
								context_instance=RequestContext(request))


# ============ Installation Procedure =====================

def install_main(request):
	"""	This view constitutes the installer process for Sylph."""
	if is_installed():
		raise Exception, "Cannot reinstall software unless data is wiped."

	user = None
	try:
		user = User.objects.get(pk=1)
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

			def make_path_uri(path = ""):
				"""Returns the URI with the port the server is running
				on, and optionally with a path segment appended."""
				# TODO: Actual hostname or external IP
				port = settings.PORT
				p = 'http://127.0.0.1%s/' % \
					("" if port == 80 else ":"+str(port))
				if path[0] == '/':
					p += path[1:]
				else:
					p += path

				if path[-1] != '/':
					p += '/'

				return p

			# Set our node endpoint URI
			node = Node.objects.get(pk=2)
			node.uri = make_path_uri('/endpoint/') # TODO: More custom
			node.protocol_version = settings.PROTOCOL_VERSION
			node.software_name = settings.SOFTWARE_NAME
			node.software_version = settings.SOFTWARE_VERSION
			node.save()

			# Save user's profile
			user.username = data['public_username']
			user.first_name = data['f_name']
			user.middle_name = data['m_name']
			user.last_name = data['l_name']
			user.email = data['email']
			user.uri = make_path_uri('/profile/') # TODO: More custom / OpenID
			user.node = node
			user.save()

			# TODO/XXX: Create site login account/credentials

			# Installation status flag is critical
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

def test(request):
	"""A view to test code. Simplifies testing process."""
	import sylph.test
	return sylph.test.test(request) # TODO/XXX: Remove in production

def test2(request):
	"""Another view to test code. Simplifies testing process."""
	import sylph.test
	return sylph.test.test2(request) # TODO/XXX: Remove in production

# ============ Signup (DEPRECATED) ========================

# /system/signup
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


