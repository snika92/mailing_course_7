from django.core.management.base import BaseCommand
from mailing.models import Mailing
from mailing.services import send_email, update_status


class Command(BaseCommand):
    help = "Отправляет письма для активных рассылок"

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status_mail="STARTED" or "CREATED")

        for mailing in mailings:
            self.stdout.write(f"Обработка рассылки: {mailing.title}")
            update_status(mailing)

            if mailing.status_mail != "COMPLETED":
                clients = mailing.clients.all()

                for client in clients:
                    send_email(mailing, client)
                    self.stdout.write(f"Письмо отправлено на {client.email} {client}")
            else:
                self.stdout.write(f"Рассылка {mailing.title} завершена и не может быть отправлена.")

        self.stdout.write(self.style.SUCCESS("Все рассылки обработаны!"))
