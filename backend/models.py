from django.db import models

# CommaSeparatedIntegerField
# DateField
# FileField, ImageField
# NullBooleanField (allows null)
# IntegerField, PositiveIntegerField
# XMLField

class Resource(models.Model):
	url = models.URLField(max_length=200)

class Post(models.Model):
	"""Post resources. Represent articles, posts, replies, etc."""
	#resource = models.ForeignKey('Resource')
	resource = models.OneToOneField('endpoint.Resource')
	reply_to = models.ForeignKey('self')

	title = models.CharField(max_length=140)
	contents = models.TextField()

	datetime_posted = models.DateTimeField()
	datetime_edited = models.DateTimeField()
	datetime_retrieved = models.DateTimeField()
	datetime_read = models.DateTimeField()

	access_uri = models.SlugField()

