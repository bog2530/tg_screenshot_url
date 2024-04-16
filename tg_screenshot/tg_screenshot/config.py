"""
Настроики приложения
"""

import enum

from pydantic import field_validator
from pydantic_settings import BaseSettings


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

    LOGGER: LoggerLevelEnum = "INFO"

    def get_mq_url(self):
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}"

    @field_validator("LOGGER")
    @classmethod
    def logger_validate(cls, v):
        if isinstance(v, str):
            return LoggerLevelEnum[v]
        return v


settings = Settings()
