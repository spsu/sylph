from datetime import datetime

def with_time(msg):
	"""Apply a timestamp to a debug message."""
	dt = datetime.now().strftime("%H:%M:%S")
	return "%s [%s]" % (msg, dt)
