from sylph.core.backend.utils.Configs import Configs

"""Constant representing untouched, uninstalled state."""
UNINSTALLED = 0

"""Constant representing touched/dirty, uninstalled state, 
eg. an unfinished install."""
UNINSTALLED_DIRTY = 1

"""Constant representing installed state."""
INSTALLED = 100

def is_installed():
	"""Determine if the Sylph instance has been installed.
	The installation procedure should be handled by the following 
	module: sylph.core.backend.views. It should create the first user
	of the system as well as login credentials. 
	"""	
	try:
		configs = Configs()
		if configs.installation_status == INSTALLED:
			print "INSTALLLLLLLED" # TODO XXX REMOVE DBG
			return True
		return False

	except Exception: # TODO: Is it wise to surpress?
		return False

