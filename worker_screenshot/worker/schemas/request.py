"""Схема данных запроса"""

import datetime
from typing import Optional

from pydantic import BaseModel


class RequestMain(BaseModel):
    """Модель первичного запроса к сервису"""

    chat_id: int
    message_id: int
    username: Optional[str]
    url: str
    date: datetime.datetime
