from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext

from sylph.apps.post.models import Post
from sylph.apps.post.tasks import post_random_message
from sylph.core.backend.models import BackendConfig
from sylph.core.backend.utils.Configs import Configs
from sylph.core.endpoint.comms.Intermediary import *
from sylph.core.resource.models import Resource

"""Quick code to test."""

def test(request):
	from sylph.core.node.api import ping_response

	return ping_response(request)
	


def test2(request):
	from sylph.utils.Communicator import Communicator

	uri = 'http://127.0.0.1:%s/system/test/' % '7000' #settings.PORT
	print uri
	comm = Communicator(uri)
	ret = comm.send_post({'dispatch': 'ping'})

	return HttpResponse(str(ret))
