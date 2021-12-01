"""Configuration initialization."""

from pathlib import Path

from cshsso.config import CONFIG, CONFIG_FILE
from cshsso.orm import DATABASE


__all__ = ['init']


def init(*, path: Path = CONFIG_FILE, db_section: str = 'db') -> None:
    """Initializes the app."""

    CONFIG.read(path)
    DATABASE.init(
        DATABASE.database,
        host=CONFIG.get(db_section, 'host'),
        user=CONFIG.get(db_section, 'user'),
        passwd=CONFIG.get(db_section, 'passwd')
    )
