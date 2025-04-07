from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from mailing.models import AttemptToSend


def send_email(mailing, client):
    """Функция отправки сообщений пользователям и занесение данных по результатам рассылки"""
    try:
        mail_response = send_mail(
            subject=mailing.message.theme,
            message=mailing.message.body,
            from_email=EMAIL_HOST_USER,
            recipient_list=[client.email],
            fail_silently=False,
        )
    except Exception as e:
        mail_response = e

    AttemptToSend.objects.create(
        status_log=(
            AttemptToSend.SUCCESS if mail_response == 1 else AttemptToSend.FAILED
        ),
        server_response=mail_response if mail_response != 1 else "",
        mailing_list=mailing,
        client=client,
    )


def update_status(mailing):
    """Функция изменения статуса рассылки с учетом текущей даты"""
    now = timezone.now()
    if mailing.finished_at < now:
        mailing.status_mail = "COMPLETED"
    elif mailing.status_mail != "COMPLETED":
        mailing.status_mail = "STARTED"
    mailing.save()
