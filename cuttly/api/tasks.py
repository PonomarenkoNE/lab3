from datetime import datetime

from celery import shared_task
from celery.result import AsyncResult
from django.core.mail import send_mail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import URL
from cuttly.settings import HOST


def call_task(data):
    res: AsyncResult = create_cutted_url.apply_async(args=(data,), countdown=0)
    res.wait(timeout=10)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'admin',
        {'type': 'send_message',
         'message': f'task: {res.task_id}, data: {res.result}, finished: {datetime.now()}, successful: {res.successful()}'}
    )


@shared_task
def create_cutted_url(data):
    new_url = URL.objects.create(original_url=data.get('original_url'), creator_id=data.get('creator'))
    new_url.cutted_url = f'{HOST}/{new_url.id}'
    new_url.save()
    send_mail('New cutted url', f'There is yours cutted url: {new_url.cutted_url}', 'callfutur@gmail.com',
              [new_url.creator.email])
    return {'username': new_url.creator.username, "cutted_url": new_url.cutted_url,
            'original_url': new_url.original_url}
