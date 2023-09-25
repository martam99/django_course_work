from smtplib import SMTPException
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from config import settings
from user.form import UserUpdateForm, UserCreation, ClientForm, ClientUpdateForm, MailingUpdate, MailingCreation
from user.models import User, Logs, Client, Mailing


# Create your views here.


class UserCreateView(CreateView):
    model = User
    form_class = UserCreation
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('user:login')

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


class UserListView(LoginRequiredMixin, ListView):
    model = User

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        raise Http404('У вас нет прав для просмотра списка пользователей данного сервиса.')


class UserDetailView(DetailView):
    model = User


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('main:general')


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
    template_name = 'user/client_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('user:client_list')


class MailCreateView(CreateView):
    model = Mailing
    form_class = MailingCreation
    template_name = 'user/mailing_form.html'
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
            Logs.objects.create(
                status='Успешно',
                date_end=Mailing.published_time,
                client=Mailing.client,
                mailing=Mailing.subject,
                error_msg='no error'
            )
        except SMTPException as err:
            Logs.objects.create(
                status='Ошибка',
                date_end=Mailing.published_time,
                client=Mailing.client,
                mailing=Mailing.subject,
                error_msg=err
            )
            return super().form_valid(form)


class MailListView(ListView):
    model = Mailing

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


class MailUpdateView(UpdateView):
    model = Mailing
    form_class = MailingUpdate
    success_url = reverse_lazy('main:general')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404
        return queryset


class MailDetailView(DetailView):
    model = Mailing


class MailDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('user:mail_list')


class LogsDetailView(DetailView):
    model = Logs
    template_name = 'user/logs_detail.html'


def toggle_activity(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse('user:user_list'))
