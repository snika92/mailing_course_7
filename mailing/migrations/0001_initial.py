# Generated by Django 5.1.7 on 2025-03-31 11:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=50, unique=True, verbose_name="Почта"),
                ),
                ("initials", models.CharField(max_length=100, verbose_name="Ф.И.О.")),
                (
                    "comment",
                    models.TextField(blank=True, null=True, verbose_name="Комментарий"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        help_text="Укажите владельца",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Владелец",
                    ),
                ),
            ],
            options={
                "verbose_name": "Клиент",
                "verbose_name_plural": "Клиенты",
                "ordering": ["email"],
            },
        ),
        migrations.CreateModel(
            name="Mailing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=200, verbose_name="Название рассылки"),
                ),
                (
                    "started_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Время начала рассылки"
                    ),
                ),
                (
                    "finished_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Время окончания рассылки"
                    ),
                ),
                (
                    "period_mail",
                    models.CharField(
                        choices=[
                            ("Ежедневная", "Ежедневная"),
                            ("Еженедельная", "Еженедельная"),
                            ("Ежемесячная", "Ежемесячная"),
                            ("Однократно", "Однократно"),
                        ],
                        default="Однократно",
                        max_length=25,
                        verbose_name="Периодичность_рассылки",
                    ),
                ),
                (
                    "status_mail",
                    models.CharField(
                        choices=[
                            ("Создана", "Создана"),
                            ("Запущена", "Запущена"),
                            ("Завершена", "Завершена"),
                        ],
                        default="Создана",
                        max_length=25,
                        verbose_name="Статус_рассылки",
                    ),
                ),
                (
                    "clients",
                    models.ManyToManyField(
                        related_name="mailing_clients",
                        to="mailing.client",
                        verbose_name="клиенты_рассылки",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        help_text="Укажите владельца сообщения",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Владелец",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
        migrations.CreateModel(
            name="AttemptToSend",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status_log",
                    models.CharField(
                        choices=[("Success", "Успешно"), ("Failed", "Не успешно")],
                        default="Success",
                        verbose_name="Статус",
                    ),
                ),
                (
                    "time_log_send",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="дата и время последней попытки"
                    ),
                ),
                (
                    "server_response",
                    models.CharField(
                        blank=True, null=True, verbose_name="ответ почтового сервера"
                    ),
                ),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mailing.client",
                        verbose_name="Клиент",
                    ),
                ),
                (
                    "mailing_list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="mailing.mailing",
                        verbose_name="Рассылка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Попытка рассылки",
                "verbose_name_plural": "Попытки рассылок",
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("theme", models.CharField(max_length=200, verbose_name="Тема письма")),
                ("body", models.TextField(verbose_name="Тело письма")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        blank=True,
                        help_text="Укажите владельца сообщения",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Владелец",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сообщение",
                "verbose_name_plural": "Сообщения",
                "ordering": ["theme"],
            },
        ),
        migrations.AddField(
            model_name="mailing",
            name="message",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="message",
                to="mailing.message",
                verbose_name="Текст_рассылки",
            ),
        ),
    ]
