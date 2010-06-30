from celery.decorators import task
from celery.task.base import PeriodicTask

from django.conf import settings

from models import BlogItem, BootstrapBlogItem
from sylph.core.node.models import Node, WebPageNode
from sylph.core.subscription.models import Subscription

from web2feed import web2feed

from datetime import datetime, timedelta

@task
def get_feed(node_id):
	"""Get the feed of 'latest' blogitem posts."""
	try:
		node = Node.objects.get(id=node_id)
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

	for item in feed:
		try:
			blog = BootstrapBlogItem()

			# uniqueness constraint prevents duplicates
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

		except Exception as e:
			print type(e)
			print e
			continue

def get_comments(blogitem_id):
	pass

# ============ Periodic Tasks =============================

class PeriodicPullBlogFeed(PeriodicTask):
	"""Periodically pull blog feeds."""

	run_every = timedelta(seconds=10)
	#run_every = timedelta(minutes=5)

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
			print "Scheduling blogfeed fetch from node %d" % node.id
			get_feed.delay(node.id)



