from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db import models

from sylph.core.endpoint.models import Resource
from sylph.apps.posts.models import Post
from sylph.core.endpoint.comms.Intermediary import *

# Quick code to test.

def test(request):
	ret = ""

	print Post.get_transportable_fields()

	posts = Post.objects.all()

	for post in posts:
		print post.get_transportable()
		print "=======================\n\n"


	store = Intermediary()

	store.addResult(posts[2])

	for d in store.data:
		#print d.appName
		#print d.modName
		#print d.data
		#print "\n\n"

		########print d.graph
		pass


	#for p in posts:
	#	ret += str(p.get_transportable())
	#	#ret += str(type(p))
	#	print type(p)
	#	print isinstance(p, Resource)
	#	ret += "\n\n"


	return HttpResponse(ret)

