from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load materials from fixture"

    def handle(self, *args, **kwargs):
        call_command("loaddata", "groups_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
