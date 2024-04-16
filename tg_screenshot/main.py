import asyncio

from tg_screenshot import dp, bot, logger


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logger.info(f"Старт")
        asyncio.run(main())
        logger.info(f"Завершен")
    except KeyboardInterrupt:
        logger.info(f"Завершен принудительно")
