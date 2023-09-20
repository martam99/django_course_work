from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from user.apps import UserConfig
from user.views import UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView, LogsDetailView, \
    ClientCreateView, ClientUpdateView, ClientListView, ClientDeleteView, MailCreateView, MailListView, MailDeleteView, \
    MailUpdateView

app_name = UserConfig.name

urlpatterns = [
    path('list/', UserListView.as_view(), name='user_list'),
    path('view/<int:pk>/', UserDetailView.as_view(), name='user_view'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('login/', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logs_view/<int:pk>/', LogsDetailView.as_view(), name='logs_view'),
    path('client_create', ClientCreateView.as_view(), name='client_create'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_list', ClientListView.as_view(), name='client_list'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('mail_create/', MailCreateView.as_view(), name='mail_create'),
    path('mail_list/', MailListView.as_view(), name='mail_list'),
    path('mail_delete/<int:pk>/', MailDeleteView.as_view(), name='mail_delete'),
    path('mail_update/<int:pk>/', MailUpdateView.as_view(), name='mail_update'),
]
