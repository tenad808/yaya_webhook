from django.urls import path
from .views import YayaWebhookView

urlpatterns = [
    path('webhook/yaya/', YayaWebhookView.as_view(), name='yaya_webhook'),
]