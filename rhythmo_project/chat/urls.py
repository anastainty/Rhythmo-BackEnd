from django.urls import path
from .views import SendMessageAPIView

urlpatterns = [
    path('api/send-message/', SendMessageAPIView.as_view(), name='send-message'),
]