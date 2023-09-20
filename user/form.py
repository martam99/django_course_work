from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from user.models import User, Client, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserCreation(UserCreationForm):
    class Meta:
        model = User
        fields = ('fullname', 'email', 'password1', 'password2', 'avatar')


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'fullname', 'comment', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('mail',)


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('mail',)


class MailingCreation(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('subject', 'body', 'published_time', 'period', 'status', 'client')


class MailingUpdate(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('subject', 'body', 'period', 'client', 'status')
