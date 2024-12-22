from django.urls import path
from .views import home_view, login_view, register_view, logout_view, welcome, reset_password_view, get_history, history_view


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='account_login'),
    path('register/', register_view, name='account_register'),
    path('logout/', logout_view, name='account_logout'),
    path('welcome/', welcome, name='welcome'),
    path('reset_password/', reset_password_view, name='reset_password'),

    path('api/history/', get_history, name='get_history'),
    path('history/', history_view, name='history'),
]