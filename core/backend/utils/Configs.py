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

			# Can only store value OR value_large (programmatically controlled)
			if conf.value_large:
				return conf.value_large
			return conf.value

		def set_val(self, key, val):
			if key in self.configs:
				if len(val) <= 255:
					conf.value = val
					conf.value_large = ""
				else:
					conf.value = ""
					conf.value_large = val

			# Create a new one.
			if len(val) <= 255:
				self.configs[key] = BackendConfig(value=val, value_large="", 
									  description="")
			else:
				self.configs[key] = BackendConfig(value="", value_large=val, 
									  description="")

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
			"""Save every object in the configuration set. SLOW. VERY SLOW"""
			# FIXME: There has to be a faster way of doing this!
			for conf in self.configs.values():
				conf.save() # SLOW!

		def delete(self, key):
			if key not in self.configs:
				raise KeyError, "Config does not exist: %s." % key
			
			conf = self.configs[key]
			conf.delete()


	# ============= Public Interface ======================

	def __init__(self):
		"""Inner class will only be instantiated once."""
		if not Configs.__INSTANCE:
			Configs.__INSTANCE = Configs.Container() 

	def __contains__(self, key):
		"""Test membership for a config key."""
		return Configs.__INSTANCE.contains(key)

	def __getitem__(self, key):
		"""Acessor. Throws exception if key doesn't exist."""
		return Configs.__INSTANCE.get_val(key)

	def __setitem__(self, key, value):
		"""Mutator. Creates new config if key doesn't exist."""
		return Configs.__INSTANCE.set_val(key, value)

	def get_description(self, key):
		"""Description accessor. Throws an exception if key doesn't exist."""
		return Configs.__INSTANCE.get_description(key)

	def set_description(self, key, value):
		"""Description mutator. Throws an exception if key doesn't exist."""
		return Configs.__INSTANCE.set_description(key, value)

	def get_full(self, key):
		"""Get value and description in a tuple.
		Throws an exception if key doesn't exist."""
		return Configs.__INSTANCE.get_full(key)

	def save(self):
		"""Save any changes made."""
		Configs.__INSTANCE.save()

	def delete(self, key):
		"""Delete a config by key."""
		Configs.__INSTANCE.delete(key)


