"""The Corps' covents."""

from enum import Enum
from typing import NamedTuple


__all__ = ['Convent']


class ConventType(NamedTuple):
    """Convent type."""

    name: str
    abbreviation: str

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return {'name': self.name, 'abbreviation': self.abbreviation}


class Convent(Enum):
    """The Corps' convents."""

    AHC = ConventType('Altherrenconvent', 'AHC')
    CC = ConventType('Corpsburschenconvent', 'CC')
    FC = ConventType('Fuchsenconvent', 'FC')
    FCC = ConventType('Feierlicher Corpsburschenconvent', 'FCC')

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return self.value.to_json()
