import traceback
from smtplib import SMTPException

from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView

from config import settings
from user.form import UserUpdateForm, UserCreation, ClientForm, ClientUpdateForm, MailingUpdate, MailingCreation
from user.models import User, Logs, Client, Mailing


# Create your views here.


class UserCreateView(CreateView):
    model = User
    form_class = UserCreation
    # template_name = 'main/user_form.html'
    # success_url = reverse_lazy('main:login')

    def form_valid(self, form):
        new_user = form.save()
        send_mail(
            subject='Поздравляем с регистрацией',
            message='Вы зарегистрировались на нашей платформе, добро пожаловать',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('main:general')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.user.save()

        return super().form_valid(form)


class UserListView(ListView):
    model = User

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.email)
        return queryset


class UserDetailView(DetailView):
    model = User


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('main:general')


class LogsDetailView(DetailView):
    model = Logs
    template_name = 'user:logs_detail.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'user/client_form.html'
    success_url = reverse_lazy('main:general')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientUpdateForm
    template_name = 'user/client_form.html'
    success_url = reverse_lazy('main:general')


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(owner=self.request.user)
        return qs


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('user:client_list')


class MailCreateView(CreateView):
    model = Mailing
    form_class = MailingCreation
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('user:mail_create')

    def form_valid(self, form):
        mail = form.save()
        try:
            send_mail(
                subject=mail.subject,
                message=mail.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[mail.client],
                fail_silently=False
            )
        except SMTPException:
            print('Ошибка:\n', traceback.format_exc())
        return super().form_valid(form)


class MailListView(ListView):
    model = Mailing

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(owner=self.request.user)
        return qs


class MailUpdateView(UpdateView):
    model = Mailing
    form_class = MailingUpdate
    # success_url = reverse_lazy('main:general')


class MailDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('user:mail_list')