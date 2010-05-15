

class User(models.Model):
	"""User resources. Represent people in the graph."""

	node = models.ForeignKey('endpoint.Node')

	username = models.CharField(max_length=30)
	email = models.EmailField()

	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)

	photo = models.ForeignKey('images.Photo')
