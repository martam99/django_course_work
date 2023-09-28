from django import template

from user.models import Mailing

register = template.Library()


@register.filter()
def mail_counts():
    mailing = Mailing.objects.all()
    return len(list(mailing))
