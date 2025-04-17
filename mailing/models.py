from django.db import models

from users.models import User


class Client(models.Model):
    email = models.EmailField(max_length=50, verbose_name="Почта")
    initials = models.CharField(max_length=100, verbose_name="Ф.И.О.")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Укажите владельца",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.initials}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["email"]


class Message(models.Model):
    theme = models.CharField(max_length=200, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Укажите владельца сообщения",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.theme}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["theme"]


class Mailing(models.Model):
    DAILY = "Ежедневная"
    WEEKLY = "Еженедельная"
    MONTHLY = "Ежемесячная"
    SINGLE = "Однократно"

    PERIOD_CHOICES = [
        (DAILY, "Ежедневная"),
        (WEEKLY, "Еженедельная"),
        (MONTHLY, "Ежемесячная"),
        (SINGLE, "Однократно"),
    ]

    CREATED = "Создана"
    STARTED = "Запущена"
    COMPLETED = "Завершена"

    STATUS_CHOICES = [
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
        (COMPLETED, "Завершена"),
    ]

    title = models.CharField(max_length=200, verbose_name="Название рассылки")
    started_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Время начала рассылки"
    )
    finished_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Время окончания рассылки"
    )
    period_mail = models.CharField(
        max_length=25,
        default=SINGLE,
        choices=PERIOD_CHOICES,
        verbose_name="Периодичность_рассылки",
    )
    status_mail = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default=CREATED,
        verbose_name="Статус_рассылки",
    )
    clients = models.ManyToManyField(
        Client, verbose_name="Клиенты_рассылки", related_name="mailing_clients"
    )
    message = models.ForeignKey(
        Message,
        related_name="message",
        verbose_name="Текст_рассылки",
        on_delete=models.PROTECT,
    )
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        help_text="Укажите владельца сообщения",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_disable_mailing", "Can disable mailing"),
        ]


class AttemptToSend(models.Model):
    SUCCESS = "Success"
    FAILED = "Failed"

    STATUS_CHOICES = [(SUCCESS, "Успешно"), (FAILED, "Не успешно")]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")
    mailing_list = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка"
    )
    status_log = models.CharField(
        choices=STATUS_CHOICES, default=SUCCESS, verbose_name="Статус"
    )
    time_log_send = models.DateTimeField(
        auto_now_add=True, verbose_name="дата и время последней попытки"
    )

    server_response = models.CharField(
        verbose_name="ответ почтового сервера", blank=True, null=True
    )

    def __str__(self):
        return f"{self.time_log_send} {self.status_log}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["status_log"]
