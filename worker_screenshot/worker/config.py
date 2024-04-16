"""
Настроики приложения
"""

import enum
from os import getenv

from pydantic import field_validator
from pydantic_settings import BaseSettings
from minio import Minio


class LoggerLevelEnum(enum.Enum):
    """
    Уровни логирования
    """

    CRITICAL = "CRITICAL"
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    WARN = "WARN"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


class Settings(BaseSettings):
    """
    Все настройки
    """

    BOT_TOKEN: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    QUEUE_NAME: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_NAME: str = ""

    MINIO_URL: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET_NAME: str

    LOGGER: LoggerLevelEnum = "INFO"

    def get_mq_url(self):
        return (
            "amqp://"
            f"{self.RABBITMQ_USER}:"
            f"{self.RABBITMQ_PASSWORD}@"
            f"{self.RABBITMQ_HOST}:"
            f"{self.RABBITMQ_PORT}"
        )

    def get_db_url(self):
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_NAME}"
        )

    def minio_client(self):
        return Minio(
            endpoint=self.MINIO_URL,
            secret_key=self.MINIO_SECRET_KEY,
            access_key=self.MINIO_ACCESS_KEY,
            secure=False,
        )

    @field_validator("LOGGER")
    @classmethod
    def logger_validate(cls, v):
        if isinstance(v, str):
            return LoggerLevelEnum[v]
        return v


settings = Settings()
