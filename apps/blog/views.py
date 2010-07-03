from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

# Models
from models import BlogItem
from sylph.core.node.models import Node
from sylph.core.subscription.models import Subscription

from datetime import datetime

def blogitem_index(request):
	"""List latest blogitems."""
	all_items = BlogItem.objects.all() \
								.order_by('-datetime_created')
	paginator = Paginator(all_items, 15) # TODO: Preference for num

	try:
		p = int(request.GET.get('page', '1'))
	except ValueError:
		p = 1

	try:
		items = paginator.page(p)
	except (EmptyPage, InvalidPage):
		raise Http404

	return render_to_response('apps/blog/index.html', {
									'items': items,													},
							context_instance=RequestContext(request))


def blogitem_create(request):
	pass

# XXX
# Instead of creating blog items in this software, let's *NOT*.
# Let's concentrate on building what this software is meant to do--
# proving that a distributed web api is useful/necessary for the 
# future.
# Let's rely on other tools--blogger, wordpress, etc.--to create 
# the blog items. Sylph will serve them, share them, and transmit 
# them around.


# XXX: This is key! Make it VERY readable.
def blogitem_view(request, item_id):
	"""View a blogitem"""
	try:
		item = BlogItem.objects.get(pk=item_id)
	except BlogItem.DoesNotExist:
		return Http404

	return render_to_response('apps/blog/view.html', {
									'item': item,
							},
							context_instance=RequestContext(request))


def blogitem_edit(request, item_id):
	pass

def blogitem_delete(request, item_id):
	pass

# =========================================================
# =========================================================
# =========================================================
# Subscription Management
# =========================================================

def subscription_index(request):

	subs = []
	try:
		subs = Subscription.objects.filter(key='blog')
	except Exception as e:
		print e
		pass

	return render_to_response('apps/blog/subscription/index.html', {
									'subscriptions': subs,
							},
							context_instance=RequestContext(request))

def subscription_view(request, subs_id):
	pass

def subscription_add(request):
	"""Add a new subscription
		1. Create Node (if doesn't exist)
		2. Create subscription
	"""

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
			node.node_type = 'Z' # NON-SYLPH! (TODO: Deprecated)
			node.node_class = 'webpage'
			node.save()

			# Create subscription
			subs = Subscription()
			subs.node = node
			subs.key = 'blog'
			subs.datetime_created = datetime.now()
			subs.is_ours = True
			subs.save()

			# Task to query node
			#tasks.do_add_node_lookup(form.cleaned_data['uri'])
			#tasks.do_add_node_lookup.delay(form.cleaned_data['uri'])

			return HttpResponseRedirect('/blog/subscription/')
	else:
		form = AddNodeForm()

	return render_to_response('apps/blog/subscription/add.html', {
									'form': form,
							},
							context_instance=RequestContext(request))

def subscription_edit(request, subs_id):
	pass

def subscription_delete(request, subs_id):
	pass


# =========================================================
# FUTURE
# =========================================================

# XXX: Automation is *key*
# I don't want to have to manually share things!
def share_blogitem(request):
	pass


