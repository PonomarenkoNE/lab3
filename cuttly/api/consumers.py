from django.shortcuts import get_object_or_404
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.decorators import database_sync_to_async
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
)

from .models import URL, User
from .consumer_serializer import URLSerializer
from .consumer_permissions import URLPermissions, is_user_logged_in
from cuttly.settings import HOST


@database_sync_to_async
def update_user_incr(user):
    if is_user_logged_in(user):
        User.objects.filter(pk=user.pk).update(is_online=True)


@database_sync_to_async
def update_user_decr(user):
    if is_user_logged_in(user):
        User.objects.filter(pk=user.pk).update(is_online=False)


class ActivityStatusConsumer:

    async def connect(self):
        await self.accept()
        await update_user_incr(self.scope['user'])

    async def disconnect(self, code):
        await update_user_decr(self.scope['user'])


class URLConsumer(ActivityStatusConsumer, GenericAsyncAPIConsumer, RetrieveModelMixin, ListModelMixin, CreateModelMixin):
    queryset = URL.objects.all()
    permission_classes = (URLPermissions, )
    serializer_class = URLSerializer

    def get_serializer_class(self, **kwargs):
        return URLSerializer

    def get_queryset(self, **kwargs):
        if kwargs.get('action') == 'list':
            urls = URL.objects.filter(creator=self.scope['user'])
            return urls
        return URL.objects.all()

    def perform_create(self, serializer, **kwargs):
        new_url = URL.objects.create(original_url=serializer.data.get('original_url'), cutted_url=serializer.data.get('cutted_url'),
                                   creator=self.scope['user'])
        new_url.cutted_url = f'{HOST}/{new_url.id}'
        new_url.save()
        return new_url
