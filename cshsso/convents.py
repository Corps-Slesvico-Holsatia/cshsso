"""The Corps' covents."""

from enum import Enum
from typing import NamedTuple


__all__ = ['Convent', 'ConventAuth']


class ConventType(NamedTuple):
    """Convent type."""

    name: str
    abbreviation: str

    def to_json(self) -> dict:
        """Returns a JSON-ish dict."""
        return {'name': self.name, 'abbreviation': self.abbreviation}


class Convent(ConventType, Enum):
    """The Corps' convents."""

    AHC = ConventType('Altherrenconvent', 'AHC')
    CC = ConventType('Corpsburschenconvent', 'CC')
    FC = ConventType('Fuchsenconvent', 'FC')
    FCC = ConventType('Feierlicher Corpsburschenconvent', 'FCC')


class ConventAuthType(NamedTuple):
    """Convent authorizations."""

    convent: Convent
    vote: bool


class ConventAuth(ConventAuthType, Enum):
    """Available convent authorizations."""

    AHC = ConventAuthType(Convent.AHC, False)
    AHC_VOTE = ConventAuthType(Convent.AHC, True)
    CC = ConventAuthType(Convent.CC, False)
    CC_VOTE = ConventAuthType(Convent.CC, True)
    FC = ConventAuthType(Convent.FC, False)
    FC_VOTE = ConventAuthType(Convent.FC, True)
    FCC = ConventAuthType(Convent.FCC, False)
    FCC_VOTE = ConventAuthType(Convent.FCC, True)
