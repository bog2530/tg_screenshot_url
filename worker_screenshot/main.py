"""
Главный модуль
"""

import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware import AsyncIO

from worker import process, settings

dramatiq.set_broker(RabbitmqBroker(url=settings.get_mq_url(), middleware=[AsyncIO()]))


@dramatiq.actor(queue_name=settings.QUEUE_NAME)
async def send_url(data: dict) -> None:
    await process(data)
