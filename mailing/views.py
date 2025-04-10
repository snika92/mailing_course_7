from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from mailing.services import send_email, update_status, get_list_by_owner

from .forms import ClientForm, MailingForm, MessageForm
from .models import AttemptToSend, Client, Mailing, Message


class HomeView(TemplateView):
    template_name = "mailing/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.groups.filter(name="managers") or user.is_superuser:
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
        if self.request.user.groups.filter(name='managers') or self.request.user.is_superuser:
            return Message.objects.order_by("-pk")
        return get_list_by_owner(self.request.user.id, Message).order_by("-pk")


@method_decorator(cache_page(60 * 15), name="dispatch")
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
        if self.request.user.groups.filter(name='managers') or self.request.user.is_superuser:
            return Client.objects.order_by("-pk")
        return get_list_by_owner(self.request.user.id, Client).order_by("-pk")


@method_decorator(cache_page(60 * 15), name="dispatch")
class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = "mailing/client_details.html"
    context_object_name = "client"


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "mailing/client_add.html"
    success_url = reverse_lazy("mailing:clients_all")
    permission_required = "mailing.add_client"

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
    permission_required = "mailing.change_client"


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
        if self.request.user.groups.filter(name='managers') or self.request.user.is_superuser:
            return Mailing.objects.order_by("-pk")
        return get_list_by_owner(self.request.user.id, Mailing).order_by("-pk")


@method_decorator(cache_page(60 * 15), name="dispatch")
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


class MailingSendMail(LoginRequiredMixin, View):
    """Класс для отправки писем пользователям"""

    model = Mailing
    template_name = "mailing/newsletter/mailing_details.html"
    context_object_name = "mailings"

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, id=pk)
        if mailing.status_mail == "COMPLETED":
            messages.error(
                request, "Рассылка не может быть инициирована, т.к. была завершена"
            )
        else:
            self.send_email(mailing, request)
            messages.success(request, "Письма отправлены!")

        return redirect("mailing:mailing_details", pk=pk)

    @staticmethod
    def send_email(mailing, request):
        clients = mailing.clients.all()
        update_status(mailing)
        if mailing.status_mail != "COMPLETED":
            for client in clients:
                send_email(mailing, client)
        else:
            messages.error(
                request,
                f"Рассылка не может быть инициирована, т.к. дата окончания рассылки {mailing.finished_at}",
            )


class LogsView(LoginRequiredMixin, ListView):
    model = AttemptToSend
    template_name = "mailing/logs.html"
    context_object_name = "logs"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='managers') or self.request.user.is_superuser:
            return queryset.order_by("-pk")
        queryset = queryset.filter(mailing_list__owner=self.request.user)
        return queryset.order_by("-pk")


class DisableMailingView(LoginRequiredMixin, View):

    def post(self, request, pk):
        mailing = get_object_or_404(Mailing, id=pk)

        if (
            not request.user.has_perm("mailing.can_disable_mailing")
            and not request.user == mailing.owner
        ):
            raise PermissionDenied("У вас нет права на отключение/включение рассылки")

        if mailing.status_mail == "COMPLETED":
            mailing.status_mail = "STARTED"
        else:
            mailing.status_mail = "COMPLETED"

        mailing.save()

        return redirect("mailing:mailing_details", pk=pk)
