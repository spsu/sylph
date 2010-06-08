

class Message(object):
	"""
	In the future, the transport framework should support:

		Node-to-Node
		------------
			* Local Node --> Remote Node
			* Remote Node --> Local Node (handling at the local side)
			* Local Node --> Many destinations (a list of destinations)
				* Must work with the task framework, also TODO

		Node-to-Service
		---------------
			* Get RDF from directory endpoints, etc.
	
		Node-to-Web
		-----------
			* Node <-- pull -- Website/Blog
				* Use web2rdf framework (also TODO) to convert to RDF)
	"""
	

	def __init__(self):
		pass

	# ============= High-level API ========================



	# ============= Lower-level API =======================



