from django.urls import re_path
from .consumers import URLConsumer

websocket_urlpatterns = [
    re_path("ws/url/", URLConsumer.as_asgi())
]