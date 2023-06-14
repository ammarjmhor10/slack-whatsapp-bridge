from django.urls import path
from .views import WhatsAppTest

urlpatterns = [
    path('whatsapp/',WhatsAppTest.as_view()),
]