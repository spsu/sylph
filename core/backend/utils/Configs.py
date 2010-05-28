# A registry-like singleton configuration object

from sylph.core.backend.models import BackendConfig

# TODO: Check that config key string matches certain conventions: r'\w+' 
# TODO: __getattr__ and __setattr__
# TODO: No way of easily making new config entries
# TODO: save() method is ***SLOW**
# TODO: Largely untested functionality. 
# TODO: Serialization mechanism to read into / out from file. 
# TODO: Cleanup the mess

class Configs(object):
	"""Configs is a singleton that accesses the Backend.Config table."""

	__INSTANCE = None

	# ============= Public Interface ======================

	def __init__(self, do_reload=False):
		"""Inner class will only be instantiated once."""
		if not Configs.__INSTANCE:
			Configs.__INSTANCE = Configs.Container() 

		if do_reload:
			Configs.__INSTANCE.reload_from_db()

	# ============= Acessors & Mutators ===================

	def __contains__(self, key):
		"""Test membership for a config key."""
		return Configs.__INSTANCE.contains(key)

	def __getattr__(self, key):
		"""Acessor. Throws exception if key doesn't exist."""
		return Configs.__INSTANCE.get_val(key)

	def __getitem__(self, key):
		"""Acessor. Throws exception if key doesn't exist."""
		return Configs.__INSTANCE.get_val(key)

	def __setattr__(self, key, value):
		"""Mutator. Creates new config if key doesn't exist."""
		return Configs.__INSTANCE.set_val(key, value)

	def __setitem__(self, key, value):
		"""Mutator. Creates new config if key doesn't exist."""
		return Configs.__INSTANCE.set_val(key, value)


	# ============= More Public API =======================

	def get_description(self, key):
		"""Description accessor. Throws an exception if key doesn't 
		exist."""
		return Configs.__INSTANCE.get_description(key)

	def set_description(self, key, value):
		"""Description mutator. Throws an exception if key doesn't 
		exist."""
		return Configs.__INSTANCE.set_description(key, value)

	def get_full(self, key):
		"""Get value and description in a tuple.
		Throws an exception if key doesn't exist."""
		return Configs.__INSTANCE.get_full(key)

	def save(self):
		"""Save any changes made. Must be called for any changes to be
		kept. At present, this is also VERY SLOW."""
		Configs.__INSTANCE.save()

	def delete(self, key):
		"""Delete a config by key."""
		Configs.__INSTANCE.delete(key)

	def reload_from_db(self):
		"""Reload the configs from the database."""
		Configs.__INSTANCE.reload()

	def __str__(self):
		return str(Configs.__INSTANCE)

	# ============= Inner Implementation ==================

	class Container(object):
		"""None of this is public interface. See below."""

		def __init__(self):
			self.configs = {}

			for config in BackendConfig.objects.all():
				self.configs[config.key] = config

		def contains(self, key):
			return key in self.configs

		def get_val(self, key):
			if key not in self.configs:
				raise KeyError, "Config does not exist: %s." % key

			conf = self.configs[key]
			typ = conf.datatype

			if typ == 'B':
				return bool(int(conf.value))
			elif typ == 'I':
				return int(conf.value)
			elif typ == 'F':
				return float(conf.value)

			# Can only store value OR value_large 
			# (This is programmatically controlled.)
			if conf.value_large:
				return conf.value_large
			return conf.value

		def set_val(self, key, val):
			if key not in self.configs:
				raise KeyError, "Config does not exist: %s." % key

			conf = self.configs[key]
			valid = {'B': bool, 'I': int, 'F': float, 'S': str}
	
			if type(val) is not valid[conf.datatype]:
				raise TypeError, "Setting config as wrong datatype: " \
								 "needed type: %s actual type: %s" % \
								 (valid[conf.datatype].__name__, 
								  type(val).__name__)

			conf.value_large = ""
	
			if conf.datatype is 'B':
				conf.value = str(int(val))
				return

			if conf.datatype in ['I', 'F']:
				conf.value = str(val)
				return

			# Can only store value OR value_large 
			# (This is programmatically controlled.)
			if len(val) <= 255:
				conf.value = val
				conf.value_large = ""
			else:
				conf.value = ""
				conf.value_large = val

			# TODO: Create a new one.
			#if len(val) <= 255:
			#	self.configs[key] = BackendConfig(value=val, value_large="", 
			#						  description="")
			#else:
			#	self.configs[key] = BackendConfig(value="", value_large=val, 
			#						  description="")

		def get_description(self, key):
			if key not in self.configs:
				raise KeyError, "Config does not exist: %s." % key

			return self.configs[key].description			

		def set_description(self, key, value):
			if key not in self.configs:
				raise KeyError, "Config does not exist: %s." % key

			self.configs[key].description = value

		def get_full(self, key):
			if key not in self.configs:
				raise KeyError, "Config does not exist: %s." % key

			conf = self.configs[key]

			value = conf.value
			if conf.value_large:
				value = sconf.value_large

			return (value, conf.description)

		def save(self):
			"""Save every object in the configuration set. SLOW. 
			VERY SLOW"""
			# FIXME: There is a faster, non-lazy way to do this.
			for conf in self.configs.values():
				conf.save() # SLOW!

		def reload_from_db(self):
			"""Reload the configs from the database."""		
			self.configs = {}
			for config in BackendConfig.objects.all():
				self.configs[config.key] = config

		def delete(self, key):
			if key not in self.configs:
				raise KeyError, "Config does not exist: %s." % key
			
			conf = self.configs[key]
			conf.delete()

		def __str__(self):
			ret = {}
			for k, v in self.configs.iteritems():
				ret[k] = self.get_val(k)
			return str(ret)

