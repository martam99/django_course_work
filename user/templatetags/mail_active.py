from django import template

from user.models import Mailing

register = template.Library()

mailing = Mailing.objects.all()


@register.filter()
def active_mail_counts():
    if mailing.status is True:
        return len(list(mailing))
