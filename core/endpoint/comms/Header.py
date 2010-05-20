
# TODO: Just use dict? 
class Header(object):

	def __init__(self, key, val):
		self.key = key
		self.val = val

	def __str__(self):
		return self.key + ": " + self.val
