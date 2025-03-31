from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(email="admin@mail.ru", username="admin")
        user.set_password("123qwerty456")
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created admin user with email {user.email}"
            )
        )
