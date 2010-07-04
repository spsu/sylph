from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext

from sylph.apps.post.models import Post
from sylph.apps.user.models import User


def test(request):
	#from sylph.core.node.api import ping_response
	#return ping_response(request)

	from sylph.utils.uri import generate_uuid
	from sylph.core.backend.models import BackendConfig
	from sylph.core.backend.utils.Configs import Configs
	from sylph.core.resource.models import Resource
	from sylph.utils.data.RdfParser import RdfParser
	from sylph.utils.data.RdfSerializer import RdfSerializer

	from sylph.utils.http import Request, Response

	req = Request('http://slashdot.org')
	resp = req.download()

	print req
	print "========"
	print req.get_headers()
	print '--------'
	print resp
	print resp.get_status()
	print '========'
	print resp.get_headers()
	print resp.get_body()


	print generate_uuid()
	print generate_uuid('posts')
	print generate_uuid('/some/path/')



	#user = User.objects.get(pk=1)

	#print user.get_transportable_fields()

	#rdf = x.to_rdf()
	#p = RdfParser(rdf)
	#udata = p.extract('User')
	#print udata


	#return HttpResponse(udata[0]['bio'])

def test2(request):
	from sylph.utils.Communicator import Communicator

	uri = 'http://127.0.0.1:%s/system/test/' % '7000' #settings.PORT

	comm = Communicator(uri)
	ret = comm.send_post({'dispatch': 'ping'})


	g = RdfParser(ret)
	data = g.extract('Node')
	print data

	return HttpResponse(str(ret))


