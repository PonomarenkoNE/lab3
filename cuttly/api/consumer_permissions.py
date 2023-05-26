from djangochannelsrestframework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser

def is_user_logged_in(user):
    return not isinstance(user, AnonymousUser)


class URLPermissions(BasePermission):
    def has_permission(self, scope, consumer, action, **kwargs):
        if action in ['create', 'list', 'retrieve'] and is_user_logged_in(scope['user']):
            return True
        return False
