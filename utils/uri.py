
def clean(uri):
	"""
	Clean URIs by mapping them onto a standard resource form.
		* Remove trailing hash
		* TODO: Remove query string?
	"""
	# TODO
	pass

def hashless(uri):
	"""Remove any trailing hash from a URI."""
	return uri.split('#')[0]
