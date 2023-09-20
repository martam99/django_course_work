from django.urls import path

from main.apps import MainConfig
from main.views import SiteTemplate

app_name = MainConfig.name

urlpatterns = [
    path('', SiteTemplate.as_view(), name='general'),
]