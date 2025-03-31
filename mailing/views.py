from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, request
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

# from .services import GameService
from .forms import ClientForm, MailingForm, MessageForm
from .models import AttemptToSend, Client, Mailing, Message


class HomeView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.groups.filter(name="managers"):
            messages_count = Message.objects.all().count()
            mailings_count = Mailing.objects.all().count()
            active_mailings_count = Mailing.objects.filter(
                status_mail="STARTED"
            ).count()
            clients_count = Client.objects.all().count()
        else:
            messages_count = Message.objects.filter(owner=user.id).count()
            mailings_count = Mailing.objects.filter(owner=user.id).count()
            active_mailings_count = Mailing.objects.filter(
                status_mail="STARTED", owner=user.id
            ).count()
            clients_count = Client.objects.filter(owner=user.id).count()
        context["messages_count"] = messages_count
        context["mailings_count"] = mailings_count
        context["active_mailings_count"] = active_mailings_count
        context["clients_count"] = clients_count
        return context


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing/messages_all.html"
    context_object_name = "messages"

    def get_queryset(self, *args, **kwargs):
        queryset = Message.objects.order_by("-pk")
        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailing/message_details.html"
    context_object_name = "message"


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_add.html"
    success_url = reverse_lazy("mailing:messages_all")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_add.html"
    success_url = reverse_lazy("mailing:messages_all")


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailing/message_delete.html"
    success_url = reverse_lazy("mailing:messages_all")

    def delete(self, request, pk):
        message = get_object_or_404(Message, id=pk)
        if (
            not request.user.has_perm("mailing.delete_message")
            and not request.user == message.owner
        ):
            raise PermissionDenied
        message.delete()


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "mailing/clients_all.html"
    context_object_name = "clients"

    def get_queryset(self, *args, **kwargs):
        queryset = Client.objects.order_by("-pk")
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "mailing/client_details.html"
    context_object_name = "client"


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_add.html"
    success_url = reverse_lazy("mailing:clients_all")

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_add.html"
    success_url = reverse_lazy("mailing:clients_all")


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = "mailing/client_delete.html"
    success_url = reverse_lazy("mailing:clients_all")

    def delete(self, request, pk):
        client = get_object_or_404(Client, id=pk)
        if (
            not request.user.has_perm("mailing.delete_client")
            and not request.user == client.owner
        ):
            raise PermissionDenied
        client.delete()


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "mailing/mailings_all.html"
    context_object_name = "mailings"

    def get_queryset(self, *args, **kwargs):
        queryset = Mailing.objects.order_by("-pk")
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "mailing/mailing_details.html"
    context_object_name = "mailing"


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_add.html"
    success_url = reverse_lazy("mailing:mailings_all")

    def get_form_kwargs(self):
        kwargs = super(MailingCreateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_add.html"
    success_url = reverse_lazy("mailing:mailings_all")

    def get_form_kwargs(self):
        kwargs = super(MailingUpdateView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "mailing/mailing_delete.html"
    success_url = reverse_lazy("mailing:mailings_all")

    def delete(self, request, pk):
        mailing = get_object_or_404(Mailing, id=pk)
        if (
            not request.user.has_perm("mailing.delete_mailing")
            and not request.user == mailing.owner
        ):
            raise PermissionDenied
        mailing.delete()


class LogsView(LoginRequiredMixin, ListView):
    model = AttemptToSend
    template_name = "mailing/logs.html"
    context_object_name = "logs"

    def get_queryset(self, *args, **kwargs):
        queryset = AttemptToSend.objects.order_by("-pk")
        return queryset
