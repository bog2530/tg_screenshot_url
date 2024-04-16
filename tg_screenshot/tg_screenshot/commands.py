"""
Команды бота
"""

import os
import re

from aiogram import Dispatcher, types, Router, Bot
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InputMediaPhoto, FSInputFile
import dramatiq

from tg_screenshot.config import settings
from tg_screenshot.logger import logger
from tg_screenshot.shemas import MessageSchema
from tg_screenshot.text import hello, unavailable
from tg_screenshot.sender import send_url

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()
router = Router()
dp.include_router(router)


@router.message(Command("start"))
async def start_handler(msg: types.Message) -> None:
    """
    При вызове /start отправить сообщение приветствие
    """
    logger.info(f"/Start chat_id: {msg.chat.id}, usrname: {msg.from_user.username}")
    await msg.answer(hello)


@router.message()
async def message_handler(msg: types.Message) -> None:
    """
    Если сообщение является ссылкой отправить в очередь
    """
    pattern = r"^(https?://)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*/?$"
    if isinstance(msg.text, str):
        if re.match(pattern, msg.text):
            data_loading = await bot.send_photo(
                msg.chat.id,
                # Костыль: Aiogram не хотел добавлять фото к сообщению без фото.
                photo=FSInputFile(path=os.path.abspath("load.png")),
                caption="Загрузка данных",
                reply_to_message_id=msg.message_id,
            )
            logger.debug(f"Message: {msg}")
            message = MessageSchema(
                chat_id=msg.chat.id,
                message_id=data_loading.message_id,
                username=msg.from_user.username,
                url=msg.text,
                date=str(msg.date),
            )
            logger.debug(f"MessageSchema: {message}")
            if not message.url.startswith("http"):
                message.url = f"http://{message.url}"
                logger.debug(f"URL: message.url")
            message_dict = message.model_dump()
            try:
                send_url.send(message_dict)
            except dramatiq.errors.ConnectionClosed:
                logger.warning("Очередь недоступна!!!!")
                await bot.edit_message_media(
                    media=InputMediaPhoto(
                        media=FSInputFile(path=os.path.abspath("error.png")),
                        caption="Сервис временно недоступен",
                    ),
                    chat_id=message.chat_id,
                    message_id=message.message_id,
                )
            else:
                logger.info(f"Отправлено в очередь: {message}")
