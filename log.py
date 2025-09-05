import logging
import coloredlogs

from enum import StrEnum, auto

log = logging.getLogger(__name__)

class LogLevel(StrEnum):
    """Stupid shit that should be in the standard lib"""
    NOTSET = auto()
    DEBUG = auto()
    INFO = auto()
    WARN = auto()
    ERROR = auto()
    CRITICAL = auto()


def configure_logging(level: LogLevel) -> None:
    coloredlogs.install(level = level.upper())
