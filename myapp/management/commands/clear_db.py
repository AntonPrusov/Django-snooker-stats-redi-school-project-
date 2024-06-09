from django.core.management.base import BaseCommand
from myapp.models import Tournament, Match  # Adjust the import according to your app name and models

class Command(BaseCommand):
    help = 'Clear all records from tournaments and matches tables'

    def handle(self, *args, **kwargs):
        # Clear tournaments
        Tournament.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all tournaments'))

        # Clear matches
        Match.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all matches'))
