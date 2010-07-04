from datetime import datetime

def with_time(msg):
	"""Apply a timestamp and color to an important debug message.
	eg. print with_time('important message')
	"""
	from sylph.utils.termcolor import colored # XXX: GPL LICENSE

	st = datetime.now().strftime("%H:%M:%S")
	st = "%s [%s]" % (msg, st)
	return colored(st, 'white', 'on_blue')

def parse_endpoint_trace(html):
	"""Return the backtrace for remote node failure.
	(This is only for use in development.)"""
	from BeautifulSoup import BeautifulSoup
	soup = BeautifulSoup(hmtl)

	# Print Trace
	soup = BeautifulSoup(html)
	trace = soup.find('textarea', id='traceback_area').string
	trace = trace.split('Traceback:')[1]
	head = 'Remote Trace for %s:\n' % str(self.uri.geturl())
	return colored(head+trace, 'yellow')

