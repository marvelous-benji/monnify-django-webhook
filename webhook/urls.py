

from django.urls import path
from .views import process_webhook, WebhookView


urlpatterns = [
    path("webhook_listen", process_webhook, name='process_webhook'),
    path('webhook_listener', WebhookView.as_view(), name='webhook_processor')
]