from django.contrib import admin

from .models import Client, Mailing, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("email", "initials", "owner")
    search_fields = ("email", "initials")
    list_filter = ("owner",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("theme", "body", "owner")
    search_fields = ("theme", "body")
    list_filter = ("owner",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "started_at",
        "finished_at",
        "period_mail",
        "status_mail",
        "owner",
    )
    search_fields = ("title",)
    list_filter = (
        "period_mail",
        "status_mail",
        "owner",
    )
