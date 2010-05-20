

# XXX: This file is just for listing ideas.

# TODO: Protocol error codes. (Flags are better than full-textual semantics.)
class ErrorCodes(object):
	"""Keep the error classes somewhat symmetrical to HTTP."""

	SUCCESSFUL = 1200

	CLIENT_ERROR = 1400
	SERVER_ERROR = 1500
	PERMISSIONS_ERROR = 1700
