from celery.decorators import task
from celery.task.base import PeriodicTask

from django.conf import settings
from django.db.models import Q

from models import BlogItem
from sylph.core.node.models import Node
from sylph.core.subscription.models import Subscription

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
		print e
		raise e

	print "fetched %d blogitems from %s" %(len(feed), node.uri)

	# uri uniqueness constraint prevents duplicates on a relational backend, 
	# but this can't occur on a non-relational system
	if not settings.IS_RELATIONAL:
		uris = []
		for item in feed:
			uris.append(item['uri'])

		blogs = BlogItem.objects.filter(uri__in=uris)
		print blogs
		duplicates = []
		for b in blogs:
			duplicates.append(b.uri)

		if duplicates:
			for k, v in feed:
				if v['uri'] in duplicates:
					del feed[k]

	for item in feed:
		try:
			blog = BlogItem()

			blog.uri = item['uri']
			blog.title = item['title']

			if 'date' in item:
				blog.datetime_created = item['date']
			if 'contents' in item:
				blog.contents = item['contents']
			if 'summary' in item:
				blog.summary = item['summary']
			if 'author' in item:
				blog.www_author_name = item['author']

			blog.save()

			# Schedule fetch of contents
			if not blog.contents:
				get_fulltext.delay(blog.pk)

		except Exception as e:
			print type(e)
			print e
			continue

@task
def get_fulltext(blogitem_id):
	"""Fetch the fulltext of a summary-only item."""
	try:
		item = BlogItem.objects.get(pk=blogitem_id)
	except BlogItem.DoesNotExist:
		print "blog.task.get_fulltext item doesn't exist"
		return

	try:
		feed = web2feed(item.uri)
	except Exception as e:
		print e
		return

	if type(feed) != dict:
		print "NOT DICT"
		return

	if feed['uri'] != item.uri:
		print "WARNING: BLOGITEM URIS DO NOT MATCH"

	if 'title' in feed:
		item.title = feed['title']
	if 'date' in feed:
		item.datetime_created = feed['date']
	if 'contents' in feed:
		item.contents = feed['contents']
	if 'author' in feed:
		item.www_author_name = feed['author']

	item.save()


def get_comments(blogitem_id):
	pass

# ============ Periodic Tasks =============================

class PeriodicPullBlogFeed(PeriodicTask):
	"""Periodically pull blog feeds."""

	#run_every = timedelta(seconds=10)
	run_every = timedelta(minutes=5)

	def run(self, **kwargs):
		print "PeriodicPullBlogFeed" # TODO: Debug
		logger = self.get_logger(**kwargs)
		logger.info("Pulling blog feeds")

		try:
			subs = Subscription.objects.filter(
									key='blog',
									is_ours=True
								)
		except Subscription.DoesNotExist:
			return

		# TODO: Respond to server overload
		for sub in subs:
			node = sub.node
			print "Scheduling blogfeed fetch from node %d" % node.pk
			get_feed.delay(node.pk)

class PeriodicUpdateSummaryOnlyItems(PeriodicTask):
	"""Periodically check for fulltext on summary-only"""

	run_every = timedelta(seconds=20)
	#run_every = timedelta(minutes=5)

	def run(self, **kwargs):
		print "PeriodicUpdateSummaryItemsOnly" # TODO: Debug
		logger = self.get_logger(**kwargs)
		logger.info("Pulling blog feeds (updating)")

		try:
			# TODO/XXX: Limit by date
			items = BlogItem.objects.filter(has_contents=False)
		except BlogItem.DoesNotExist:
			return

		print items

		# TODO: Respond to server overload
		for item in items:
			get_fulltext.delay(item.pk)

