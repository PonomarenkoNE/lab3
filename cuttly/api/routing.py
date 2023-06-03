from django.urls import re_path
from .consumers import URLConsumer, AdminConsumer

websocket_urlpatterns = [
    re_path("ws/url/", URLConsumer.as_asgi()),
    re_path(r'ws/monitor/$', AdminConsumer.as_asgi())
]