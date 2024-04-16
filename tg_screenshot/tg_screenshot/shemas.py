"""
Схемы
"""

from typing import Optional

from pydantic import BaseModel


class MessageSchema(BaseModel):
    """
    Схема сообщения
    """

    chat_id: int
    message_id: int
    username: Optional[str]
    url: str
    date: str
