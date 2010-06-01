from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from models import *
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
		node = Node.objects.get(pk=1)
	except Node.DoesNotExist:
		raise Http404 # TODO: This is actually a core system failure!

	class EditNodeForm(forms.ModelForm):
		"""Form for editing one's own node"""
		class Meta:
			model = Node
			fields = ['uri', # TODO: Should we let them edit URI this way?
					  'name', 'description']

	if request.method == 'POST':
		form = EditNodeForm(request.POST, instance=node)
		if form.is_valid():
			n = form.save(commit=False)
			n.datetime_edited = datetime.today()
			n.save()
			return HttpResponseRedirect('/node/view/1/')

	else:
		form = EditNodeForm(instance=node)

	return render_to_response('core/node/edit_own.html',
							  {'form': form}, 
							  context_instance=RequestContext(request))


# ============ Edit Other Node ============================

def edit_other_node(request, node_id):
	"""Edit the details on another node that isn't our own."""
	if node_id in [1, '1']:
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
			node_uri = '/node/view/%d/' % node.id
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
			tasks.do_add_node_lookup(form.cleaned_data['uri'])
			#tasks.do_add_node_lookup.delay(form.cleaned_data['uri'])

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
	if node_id in [1, '1']:
		return HttpResponseRedirect('/node/view/1/')

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


