from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core import serializers
from django.conf import settings

from models import *
from sylph.core.resource.models import Resource
import tasks

from datetime import datetime
import hashlib


# ============ Node Index ===============================

def index(request):
	nodes = Node.objects.all()
	return render_to_response('core/node/index.html', {
									'nodes': nodes,
							},
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


# ============ Edit Own Node ==============================

def edit_own_node(request):
	"""Edit the details on our own node."""
	node = None
	try:
		node = Node.objects.get(pk=settings.OUR_NODE_PK)
	except Node.DoesNotExist:
		raise Http404 # TODO: This is actually a core system failure!

	class EditNodeForm(forms.ModelForm):
		"""Form for editing one's own node"""
		class Meta:
			model = Node
			fields = [#'uri', # TODO: Should we let them edit URI this way?
								# XXX: ALSO! IT SEEMS TO NOT WORK NOW!
						'name',
						'description']

	class EditNodeUriForm(forms.ModelForm):
		"""Form to edit your node URI
		This is a workaround since Django won't do it for us!"""
		class Meta:
			model = Node
			fields = ['uri']

	if request.method == 'POST':
		form = EditNodeForm(request.POST, instance=node)
		res_form = EditNodeUriForm(request.POST, instance=node)

		if 'uri' in request.GET:
			node.uri = request.POST['uri'] # FIXME: Not clean, but form failed!
			node.datetime_edited = datetime.today()
			node.save()
			return HttpResponseRedirect('/node/view/2/')

		else:
			if form.is_valid():
				n = form.save(commit=False)
				n.datetime_edited = datetime.today()
				n.save()
				return HttpResponseRedirect('/node/view/2/')

	else:
		form = EditNodeForm(instance=node)
		res_form = EditNodeUriForm(instance=node)

	return render_to_response('core/node/edit_own.html', {
									'form': form,
									'res_form': res_form
								},
								context_instance=RequestContext(request))


# ============ Edit Other Node ============================

def edit_other_node(request, node_id):
	"""Edit the details on another node that isn't our own."""
	if node_id in [1, '1', 2, '2']:
		return HttpResponseRedirect('/node/edit/')

	node = None
	try:
		node = Node.objects.get(pk=node_id)
	except Node.DoesNotExist:
		raise Http404

	class EditOtherNodeForm(forms.ModelForm):
		"""Form for editing another node"""
		class Meta:
			model = Node
			fields = ['own_description']

	if request.method == 'POST':
		form = EditOtherNodeForm(request.POST, instance=node)
		if form.is_valid():
			# Note: Don't change datetime_edited--that's only for owner
			n = form.save(commit=False)
			n.save()
			node_uri = '/node/view/%d/' % node.pk
			return HttpResponseRedirect(node_uri)

	else:
		form = EditOtherNodeForm(instance=node)

	return render_to_response('core/node/edit_other.html',
								{'node': node, 'form': form},
								context_instance=RequestContext(request))


# ============ View Node ===============================

def view_node(request, node_id):
	"""View a node status page"""
	node = None
	try:
		node = Node.objects.get(pk=node_id)
	except Node.DoesNotExist:
		raise Http404

	return render_to_response('core/node/view.html', {
									'node': node,
							},
							context_instance=RequestContext(request),
							mimetype='application/xhtml+xml')


# ============ Add Node ===================================

#@login_required
def add_node(request):
	"""Create a new post."""
	# TODO: Try Celery to asynch request/poll the node. 

	class AddNodeForm(forms.ModelForm):
		"""Form for adding nodes"""
		class Meta:
			model = Node
			fields = ['uri', 'own_description']

	if request.method == 'POST':
		form = AddNodeForm(request.POST)
		if form.is_valid():
			node = form.save(commit=False)
			node.datetime_added = datetime.today()
			node.is_yet_to_resolve = True
			node.status = 'U'
			node.save()

			# Task to query node
			#tasks.do_add_node_lookup(form.cleaned_data['uri'])
			tasks.do_add_node_lookup.delay(form.cleaned_data['uri'])

			return HttpResponseRedirect('/node/')
	else:
		form = AddNodeForm()

	return render_to_response('core/node/add.html', {
								'form': form
								},
								context_instance=RequestContext(request))


# ============ Delete Node ================================

def delete_node(request, node_id):
	"""Delete a node from the system."""
	if node_id in [1, '1', 2, '2']:
		return HttpResponseRedirect('/node/view/2/')

	node = None
	try:
		node = Node.objects.get(pk=node_id)
	except Node.DoesNotExist:
		raise Http404

	if request.method == 'POST':
		node.delete()
		return HttpResponseRedirect('/node/')

	return render_to_response('core/node/delete.html',
								context_instance=RequestContext(request))


# ============ Ajax =======================================

def ajax_get_info(request):
	"""Returns info for the requested nodes."""
	#if not request.is_ajax():
	#	return HttpResponse('')

	nodes = serializers.serialize("json", Node.objects.all())
	return HttpResponse(nodes)
