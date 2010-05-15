# Jobs for the post system. 

def prunePosts(): pass
	# Prune old posts (that aren't saved) from the system

def checkFeedForThreads(): pass
	# Check a feed (or site?) for threads

def checkThreadForReplies(): pass
	# Check a thread for replies. 

# XXX: This probably belongs elsewhere, such as in social or endpoint:
def checkEndpointForNewResources(): pass
	# Not even sure how to do this effectively yet
	# Do I try to get all new resources? Only one type? Whatever the
	# endpoint is willing to tell us, or a specific target?
		# XXX: Where does this code belong?
		# XXX: Need an endpoint resolver class, 
			# payload class (supporting encryption), 
			# resource (after unloaded) class. -- or is that the model?
