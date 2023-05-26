from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path

from .views import *

urlpatterns = [
    path('create-user/', UserCreationView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('url/<uuid:id>/', URLView.as_view({'get': 'get', 'patch': 'patch', 'delete': 'delete'})),
    path('url/', URLView.as_view({'post': 'post'})),
    path('my-urls/', MyURLsView.as_view())
]