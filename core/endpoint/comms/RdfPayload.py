from Intermediary import Intermediary

# THIS IS THE POSTDATA!
# TODO: Add another layer for encryption. 

class RdfPayload(object):
	"""This is the serialization format that travels through the internet!

	Simplified Communication model:
		NODE_A <-> Intermediary <-> RdfPayload <-> Intermediary <-> NODE_B
	"""

	def __init__(self, p = None)
		# TODO: Determine if p is a string (incoming) or Intermediary (outgoing)
		pass

	def toIntermediary(self):
		# TODO: Convert back into pre-payload form. 
		return Intermediary( TO_DO )

	def getSerialized(self):
		# TODO: Gets the serialized form
		return "<rdf>Serialized Data</rdf>"
