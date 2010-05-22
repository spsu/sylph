from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from sylph.core.endpoint.models import Resource
from sylph.apps.posts.models import Post

# Quick code to test.

def test(request):

	posts = Post.objects.all()

	ret = ""
	for p in posts:
		ret += str(p.get_transportable())
		ret += "\n\n"


	return HttpResponse(ret)
