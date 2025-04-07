from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Load materials from fixture'

    def handle(self, *args, **kwargs):
        call_command('loaddata', 'groups_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
