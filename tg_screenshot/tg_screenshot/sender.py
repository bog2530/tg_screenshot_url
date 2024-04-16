"""
Отправка в очередь
"""

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware import AsyncIO

from tg_screenshot.config import settings


dramatiq.set_broker(RabbitmqBroker(url=settings.get_mq_url(), middleware=[AsyncIO()]))


@dramatiq.actor(queue_name=settings.QUEUE_NAME)
async def send_url(*args, **kwargs):
    """
    Отправка в очередь
    """
    pass
