import logging
import socket

from celery import log
from celery.messaging import establish_connection, get_consumer_set
from celery.worker.job import TaskRequest

"""
Code is from Ask
"""

class CronCelery(object):
	hostname = socket.gethostname()

	def __init__(self, logger=None):
		self.logger = log.get_default_logger(loglevel=logging.INFO)
		self._setup_consumer()

	def _setup_consumer(self):
		self.connection = establish_connection()
		self.consumer = get_consumer_set(self.connection)

	def close(self):
		self.consumer.close()
		self.connection.close()

	def process_n(self, n=1):
		for i in xrange(n):
			#message = self.consumer.fetch()
			consumer = self.consumer.consumers[0]
			message = consumer.fetch()
			if message is None:
				# No more messages for us
				return
			self.on_message(message.payload, message)
		
	def on_message(self, message_data, message):
		try:
			task = TaskRequest.from_message(message, message_data,
											logger=self.logger,
											hostname=self.hostname)
		except Exception, exc:
			message.ack()
			raise

		task.execute()

