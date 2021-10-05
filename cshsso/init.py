"""Configuration initialization."""

from cshsso.config import CONFIG, CONFIG_FILE
from cshsso.orm import DATABASE


__all__ = ['init']


def init() -> None:
    """Initializes the app."""

    CONFIG.read(CONFIG_FILE)
    DATABASE.init(
        DATABASE.database,
        host=CONFIG.get('db', 'host'),
        user=CONFIG.get('db', 'user'),
        passwd=CONFIG.get('db', 'passwd')
    )
