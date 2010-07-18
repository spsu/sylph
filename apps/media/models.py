from django.db import models
from django.core.files import File
from django.core.files.base import ContentFile

from sylph.core.resource.models import Resource
from sylph.core.resource.models import register_type

from StringIO import StringIO
import Image as PilImage # XXX: Is this okay?
from datetime import datetime
import hashlib # python 2.5

# ============ File Model =======================

class File(Resource):

	"""Cryptographic hash of the file contents."""
	sha1_hexdigest = models.CharField(max_length=40, blank=False, null=False)

	"""The actual file, if it is locally stored."""
	cached = models.FileField(upload_to='%Y/%m/%d', blank=True, null=False)

	mimetype = models.CharField(max_length=40, blank=False, null=False)

	@classmethod
	def new_from_message(cls, message, save=True):
		if message.is_image():
			return Image.new_from_message(message, save)

		# TODO: Other types

# ============ Image Model ======================

class Image(File):

	"""Dimensions of the image."""
	width = models.IntegerField(blank=False, null=False)
	height = models.IntegerField(blank=False, null=False)

	@classmethod
	def new_from_message(cls, message, save=True):
		"""Create a new Image from a message."""
		r = Image()
		r.uri = message.get_uri()
		#self.datetime_created = 0
		#self.datetime_edited = 0
		r.datetime_added = datetime.today()
		r.mimetype = message.get_content_type()

		hsh = hashlib.sha1(message.get_body()).hexdigest() 
		f = ContentFile(message.get_body())

		im = PilImage.open(StringIO(message.get_body()))
		r.width = im.size[0]
		r.height = im.size[1]
		del im

		r.cached.save(hsh, f, save=False)
		r.sha1_hexdigest = hsh

		if save:
			r.save()

		return r

# ============ Video Model ======================

class Video(File):

	"""Dimensions of the video."""
	width = models.IntegerField(blank=False, null=False)
	width = models.IntegerField(blank=False, null=False)

	# XXX: Probably the wrong way to do this...
	length = models.IntegerField(blank=False, null=False)

# ============ Audio Model ======================

class Audio(File):

	# XXX: Probably the wrong way to do this... 
	length = models.IntegerField(blank=False, null=False)


register_type(File)
register_type(Image)
register_type(Video)
register_type(Audio)

