from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from user.models import User, Client, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserCreation(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('fullname', 'email', 'password1', 'password2', 'avatar')


class UserUpdateForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'fullname', 'comment', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('mail',)


class ClientUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('mail',)


class MailingCreation(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('subject', 'body', 'published_time', 'period', 'status', 'client')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'status':
                field.widget.attrs['class'] = 'form-control'


class MailingUpdate(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('subject', 'body', 'period', 'client', 'status')
