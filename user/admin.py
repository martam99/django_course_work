from django.contrib import admin

from user.models import User, Client

# Register your models here.
admin.site.register(User)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'mail', 'comment', 'owner')