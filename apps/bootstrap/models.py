from django.db import models
from sylph.apps.blog.models import BlogItem
from sylph.core.resource.models import Resource

#class SiteAccount(models.Model):
#	# TODO: Bootstrap Comments / Site social features
#	pass


#class NewsItem(models.Model):
#	pass


#class Response(post.Post):
#	# TODO: Bootstrap Comments 
#	pass

class Site(Resource): # TODO: Could a site be a 'dumb node' instead? 
	"""
	A Site (an index page) that will be scraped for content.

	The URL will be checked against existing rules in web2py 
	(which is another software package I am writing), and if not found
	then generic heuristics will be used to scrape probable story urls.

	There will be different types of fetched content
		* BlogItems
		* Pages (typically static; text + optional images) IMPORTANT!
		* Wiki
		* Profile (profile pages for eg. forums, reddit, etc. with no 
				   specific algorithm to parse/support)
		* Some kind of fact/knowledge base
		* Bootstrapped manuals for programming, etc? (That'd be nice..)
		* Etc... we'll figure it out as we go along 

	(NEEDS TO BE EASY TO MAINTAIN ALL OF THIS!)
	"""	

	# ============= Sylph Metadata ========================

	rdf_fields = [
		'title',
		'description',
	]


	# ============= Model Fields ==========================

	"""Title of the website."""
	title = models.CharField(max_length=25, blank=True, null=False)

	"""Optional textual description of the site."""
	description = models.CharField(max_length=100, blank=True, null=False)

	# TODO: Timedelta conversion to float
	# http://stackoverflow.com/questions/801912/
	# how-to-put-timedelta-in-django-model
	update_every = models.FloatField(blank=True, null=False)

	# TODO: md5 of page contents to see when it was last updated?

	# TODO
	# thumbnail = models.???
	# thumbnail_date

	# TODO -- images for logo and icon
	logo = models.CharField(max_length=25, blank=True, null=False)
	icon = models.CharField(max_length=25, blank=True, null=False)

#class SiteFeed(models.Model):
#	"""Every site has one or more categorical feeds, (even if it 
#	only has one.) This allows us to fine-tune/narrow what we fetch."""
#
#	site = models.ForeignKey(Site)
#
#	"""A key that denotes how to access the feed if a scraping or 
#	parsing ruleset exists for the site."""
#	key = models.CharField(max_length=25, blank=True, null=False)
#
#	"""The human-readable name of the feed. 
#	Eg, "Main Feed", "Science", or "Sports"."""
#	name = models.CharField(max_length=30, blank=True, null=False)
#

class BootstrapBlogItem(BlogItem):
	"""
	A BlogItem that is retrieved from a 'dumb' website (with no
	semantic cabability). 

	Will also have:
		* Author[s]
		* Comments
		* Photos/Gallery
		* Rating (there are different scales depending on the site)
	"""

	# ============= Sylph Metadata ========================

	rdf_fields = [
		'site',
	]


	# ============= Model Fields ==========================

	site = models.ForeignKey('Site')


