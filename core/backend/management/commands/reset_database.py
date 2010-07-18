from django.core.management.base import BaseCommand, CommandError

from sylph.utils.database import reset_database

class Command(BaseCommand):
	args = ''
	help = 'Reset the database'

	def handle(self, *args, **options):
		reset_database()
		print "Database reset."
