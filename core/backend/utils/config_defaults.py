"""
	Creates the default configuration options and supplies the default 
	values.
"""

from Configs import Configs

# TODO: Currently this documents what configuration options need creating. 

# TODO: Should userinfo or privacy options go here, or do they belong in their
# own modules?

def create_main():

	changed = False
	configs = Configs()

	defs = {

		# ===== High Priority ====

		# ===== Med Priority =====

		# ===== Low Priority =====

		'per_page_fulltext': (15, 
			'The number of items to show per page for fulltext articles/posts'),

		'per_page_list': (25,
			'The number of items to show per page for lists of items'),

	}


