
"""
These views allow us to view and manage the sites we wish to scrape
content from. Nothing more.

Perhaps we want to present users a few options for default sites to
scrape: New York Times, Slashdot, etc. 

Note: see my web2rdf project (also on my github) to see how that will
integrate here. 
"""

def index(request):
	"""View a list of the sites added to the system."""
	pass


def add_site(request):
	"""Add a website to scrape for content."""
	pass


def view_site(request, site_id):
	"""View the stats on a site: number of articles fetched, saved,
	ratings thereof, last fetched date, etc."""
	pass


def edit_site(request, site_id):
	"""Edit site notes and change the schedule."""
	pass


def delete_site(request, site_id):
	"""Delete a site from the bootstrap system. (References to it
	may still exist.)"""
	pass


