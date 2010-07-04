from models import *

def auto_apply_resource_type(sender, instance, **kwargs):
	"""Automatically apply the type to the resource"""
	res = instance
	if res.resource_type and res.resource_type != 'TODO':
		return

	name = str(type(res))
	try:
		name = name.strip('<>\'\"').split('.')[-1]
	except Exception as e:
		print e
		pass

	res.resource_type = name

