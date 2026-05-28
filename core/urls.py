from django.urls import path
from .views import send_to_telegram

urlpatterns = [
    path('', send_to_telegram, name='home'),
]