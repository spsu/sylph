from models import *

def auto_apply_resource_type(sender, instance, **kwargs):
	"""Automatically apply the type to the resource"""
	print "signal: auto_apply_type"
	res = instance
	if res.resource_type:
		return

	name = str(type(res))
	print name
	try:
		name = name.strip('<>\'\"').split('.')[-1]
		print name
	except Exception as e:
		print e
		pass

	res.resource_type = name


