from celery.decorators import task
from celery.task.base import PeriodicTask

from django.conf import settings
from django.db.models import Q

from models import BlogItem
from sylph.core.node.models import Node
from sylph.core.subscription.models import Subscription
from sylph.utils.debug import with_time

from web2feed import web2feed

from datetime import datetime, timedelta

@task
def get_feed(node_id):
	"""Get the feed of 'latest' blogitem posts."""
	try:
		node = Node.objects.get(pk=node_id)
	except Node.DoesNotExist:
		print "blog.task.get_feed failure: node %d doesn't exist" % node_id
		return

	# XXX: This is only for Bootstrapped blog items
	# When blogitems are shared in sylph (very soon), then we'll use
	# the sylph protocol
	try:
		feed = web2feed(node.uri)
	except Exception as e:
		node.just_failed(save=True)
		print e
		raise e

	# XXX: I really need a wrapper around *all* node comms.
	node.just_pulled_from(save=True)

	print "fetched %d blogitems from %s" %(len(feed), node.uri)

	for item in feed:
		try:
			blog = BlogItem()

			# uniqueness constraint prevents duplicates
			blog.uri = item['uri']
			blog.title = item['title']

			if 'date' in item:
				blog.datetime_created = item['date']
			if 'contents' in item and item['contents']:
				blog.contents = item['contents']
				blog.has_contents = True
			if 'summary' in item and item['summary']:
				blog.summary = item['summary']
				blog.has_summary = True
			if 'author' in item:
				blog.www_author_name = item['author']

			blog.save()

			# Schedule fetch of contents
			if not blog.contents:
				get_fulltext.delay(blog.pk)

		except Exception as e:
			exp = str(type(e))
			if 'IntegrityError' in exp:
				continue
			print e # DEBUG
			continue

@task
def get_fulltext(blogitem_id):
	"""Fetch the fulltext of a summary-only item."""
	try:
		item = BlogItem.objects.get(pk=blogitem_id)
	except BlogItem.DoesNotExist:
		print "blog.task.get_fulltext item doesn't exist"
		return

	item.tried_fetch_count += 1 # XXX: Verify increment works

	try:
		feed = web2feed(item.uri)
		if not feed or type(feed) != dict:
			raise Exception, "web2feed did not return a dictionary."
	except Exception as e:
		print e
		item.save()
		return

	if feed['uri'] != item.uri:
		print "WARNING: BLOGITEM URIS DO NOT MATCH"

	if 'title' in feed:
		item.title = feed['title']
	if 'date' in feed:
		item.datetime_created = feed['date']
	if 'contents' in feed and feed['contents']:
		item.contents = feed['contents']
		item.has_contents = True
	if 'author' in feed:
		item.www_author_name = feed['author']

	item.save()


def get_comments(blogitem_id):
	pass

# ============ Periodic Tasks =============================

class PullBlogFeeds(PeriodicTask):
	"""Periodically pull blog feeds."""

	#run_every = timedelta(seconds=10)
	run_every = timedelta(minutes=5)

	def run(self, **kwargs):
		print with_time("blog.PeriodicPullBlogFeed") # TODO: Debug

		# TODO XXX XXX XXX: LIMIT TO ONLY 5 AT A TIME!
		subs = Subscription.objects.filter(
										key='blog',
										is_ours=True
									)

		# TODO: Respond to server overload
		for sub in subs:
			node = sub.node
			print "\t...Scheduling blogfeed fetch from node %d" % node.pk
			get_feed.delay(node.pk)

class UpdateSummaryOnlyItems(PeriodicTask):
	"""Periodically check for fulltext on summary-only"""

	run_every = timedelta(seconds=20)
	#run_every = timedelta(minutes=5)

	def run(self, **kwargs):
		print with_time("blog.PeriodicUpdateSummaryItemsOnly") # TODO: Debug

		# XXX: Limit to a smaller number...
		items = BlogItem.objects.filter(has_contents=False) \
								.filter(tried_fetch_count__lt=5)

		# TODO: Respond to server overload
		for item in items:
			get_fulltext.delay(item.pk)

