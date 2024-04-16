"""
Воркер
"""

import datetime
import os
from zoneinfo import ZoneInfo
from urllib.parse import urlparse

from aiogram.types import BufferedInputFile, InputMediaPhoto, FSInputFile
from pydantic_core import ValidationError

from worker.schemas import RequestMain
from worker.dependencies import bot, get_async_repository, get_minio_storage
from worker.screenshot import screenshot
from worker.db import Statistics
from worker.logger import logger


async def process(data: dict) -> None:
    """
    Обработка данных, получение скриншота, сохранение в БД и MinIO, отправка пользователю
    """
    try:
        logger.debug(data)
        parsed_request = RequestMain.model_validate(data)
        logger.debug(parsed_request)
    except (ValidationError, ValueError):
        logger.warning(f"Полученные данные невалидны")
        logger.debug(data)
    else:
        try:
            title, page, file = await screenshot(parsed_request.url)
        except:
            await get_async_repository().save(
                Statistics(
                    username=parsed_request.username,
                    chat_id=str(parsed_request.chat_id),
                    url=parsed_request.url,
                    date=parsed_request.date,
                )
            )
            await bot.edit_message_media(
                media=InputMediaPhoto(
                    media=FSInputFile(path=os.path.abspath("error.png")),
                    caption="Страница не найдена"
                ),
                chat_id=parsed_request.chat_id,
                message_id=parsed_request.message_id,
            )
            logger.debug("Ошибка загрузки картинки")
        else:
            netloc = urlparse(parsed_request.url)
            filename = f"{str(parsed_request.date)}_{parsed_request.chat_id}_{netloc.netloc}.png"
            try:
                get_minio_storage().upload_file(filename, file)
            except:
                logger.warning(f"Проблемы с минио!!!!")
            else:
                await get_async_repository().save(
                    Statistics(
                        username=parsed_request.username,
                        chat_id=str(parsed_request.chat_id),
                        url=parsed_request.url,
                        screenshot=filename,
                        date=parsed_request.date,
                    )
                )
                end = datetime.datetime.now(ZoneInfo("UTC"))
                diff = end - parsed_request.date
                text = f"{title}\nВеб-сайт: {page}\nВремя выполнения: {diff.seconds} cек."
                await bot.edit_message_media(
                    media=InputMediaPhoto(
                        media=BufferedInputFile(file, "img.png"), caption=text
                    ),
                    chat_id=parsed_request.chat_id,
                    message_id=parsed_request.message_id,
                )
                logger.info(f"Отправлено: {text}, Картинка: {filename}")
