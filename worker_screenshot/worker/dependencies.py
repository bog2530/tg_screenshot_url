from aiogram import Bot

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from worker.db import BaseRepository
from worker.config import settings
from worker.minio import MinioStorage

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


def get_async_repository() -> BaseRepository:
    return BaseRepository(settings.get_db_url())


def get_minio_storage() -> MinioStorage:
    if not settings.minio_client().bucket_exists(settings.MINIO_BUCKET_NAME):
        settings.minio_client().make_bucket(settings.MINIO_BUCKET_NAME)
    return MinioStorage(settings.minio_client(), settings.MINIO_BUCKET_NAME)
