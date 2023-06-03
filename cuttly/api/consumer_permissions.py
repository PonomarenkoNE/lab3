from djangochannelsrestframework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser

from .models import User

def is_user_logged_in(user):
    return not isinstance(user, AnonymousUser)

def is_user_admin(user):
    if isinstance(user, User):
        return user.is_superuser


class URLPermissions(BasePermission):
    def has_permission(self, scope, consumer, action, **kwargs):
        if action in ['create', 'list', 'retrieve'] and is_user_logged_in(scope['user']):
            return True
        return False
