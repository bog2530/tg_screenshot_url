"""
Логирование
"""

import logging

from worker.config import settings

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOGGER.value)
