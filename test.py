from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db import models

from sylph.core.resource.models import Resource
from sylph.core.endpoint.comms.Intermediary import *
from sylph.core.backend.models import BackendConfig
from sylph.core.backend.utils.Configs import Configs
from sylph.apps.post.models import Post

from sylph.apps.post.tasks import post_random_message


# Quick code to test.

def test(request):
	ret = ""

	result = post_random_message.delay()

	print result

	return HttpResponse(ret, mimetype='text/plain')
	


def test2(request):
	ret = "asdf\nasdf"

	#print Post.get_transportable_fields()

	posts = Post.objects.all()

	#for post in posts:
	#	print post.get_transportable()
	#	print "=======================\n\n"


	store = Intermediary()

	store.addResult(posts)

	ret = str(store.toRdf())

	return HttpResponse(ret, mimetype='text/plain')

