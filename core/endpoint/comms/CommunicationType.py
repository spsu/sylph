# From the endpoint decoder:
# CommunicationTypeUri -> Dispatcher -> Code To Handle
# 											|
#			   Propagation to client   <-----
#
# >>>> OR IF NOT FOUND
#
# CommunicationTypeUri -> Dispatcher (NOT FOUND)
# 								|
#	  Propagation to client  <---
#

class CommunicationType(object):

	pass

***** Resource can be response to other resource!

Rating is_a resource technically, but SHOULD NOT be represented as_a_resource.

* Push post (generic)
* Push response [to post, image, etc]
* Push image

* Push latest profile (whole thing OR diff?)

# /sylph/push/profile
	* Pushes ENTIRE profile (but thats not_much information!)
	* pushing profile diffs TOO_COMPLEX at present

# /sylph/push/post
	* Push a post we made somewhere.
	* Should it contain reply to? Or should we... 
		# /sylph/push/reply

RESPONSES:

# /sylph/response/accepted
# /sylph/response/rejected
	* Dont do more dynamic permission reasons. These will be later.
# /sylph/response/not-understood
# /sylph/response/client-error
# /sylph/response/server-error

	^^^ All of these reasons may require additonal elaboration. 


