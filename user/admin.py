from django.contrib import admin

from user.models import User, Client, Mailing, Logs

# Register your models here.
admin.site.register(User)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'mail', 'comment', 'owner')


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('published_time', 'period', 'status', 'subject', 'body', 'owner')


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('status', 'mailing', 'error_msg')
