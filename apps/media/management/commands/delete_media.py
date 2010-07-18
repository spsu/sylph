from django.core.management.base import BaseCommand, CommandError
from sylph.utils.file import delete_uploads 

class Command(BaseCommand):
	args = ''
	help = 'Delete media'

	def handle(self, *args, **options):
		delete_uploads()
		print "Media deleted."

