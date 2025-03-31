from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import HomeView

from .views import (ClientCreateView, ClientDeleteView, ClientDetailView,
                    ClientListView, ClientUpdateView, LogsView,
                    MailingCreateView, MailingDeleteView, MailingDetailView,
                    MailingListView, MailingUpdateView, MessageCreateView,
                    MessageDeleteView, MessageDetailView, MessageListView,
                    MessageUpdateView)

app_name = MailingConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("messages_all/", MessageListView.as_view(), name="messages_all"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_details"),
    path("message_add/", MessageCreateView.as_view(), name="message_add"),
    path("message/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_update"),
    path(
        "message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"
    ),
    path("clients_all/", ClientListView.as_view(), name="clients_all"),
    path("client/<int:pk>/", ClientDetailView.as_view(), name="client_details"),
    path("client_add/", ClientCreateView.as_view(), name="client_add"),
    path("client/<int:pk>/edit/", ClientUpdateView.as_view(), name="client_update"),
    path("client/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
    path("mailings_all/", MailingListView.as_view(), name="mailings_all"),
    path("mailing/<int:pk>/", MailingDetailView.as_view(), name="mailing_details"),
    path("mailing_add/", MailingCreateView.as_view(), name="mailing_add"),
    path("mailing/<int:pk>/edit/", MailingUpdateView.as_view(), name="mailing_update"),
    path(
        "mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path("logs", LogsView.as_view(), name="logs"),
]
