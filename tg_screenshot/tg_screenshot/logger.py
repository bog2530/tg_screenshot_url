"""
Логирование
"""

import logging
import sys

from tg_screenshot.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOGGER.value)

handler_stdout = logging.StreamHandler(stream=sys.stdout)
handler_stdout.setFormatter(
    logging.Formatter(fmt="[%(asctime)s;%(levelname)s;TG_BOT;] %(message)s")
)

logger.addHandler(handler_stdout)
