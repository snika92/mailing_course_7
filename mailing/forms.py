from django.forms import (BooleanField, ModelForm, ModelMultipleChoiceField,
                          SelectMultiple)

from mailing.models import Client, Mailing, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ["created_at", "updated_at", "owner"]


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ["created_at", "updated_at", "owner"]


class MailingForm(StyleFormMixin, ModelForm):

    def __init__(self, *args, **kwargs):
        the_user = kwargs.pop("user", None)
        super(MailingForm, self).__init__(*args, **kwargs)
        qs_clients = Client.objects.filter(owner=the_user)
        if the_user is not None:
            self.fields["message"].queryset = the_user.message_set.all()
            self.fields["clients"] = ModelMultipleChoiceField(
                queryset=qs_clients, widget=SelectMultiple, label="Клиенты"
            )

    class Meta:
        model = Mailing
        exclude = ["started_at", "owner", "status_mail"]
