"""The Corps' covents."""

from enum import Enum
from typing import Any, NamedTuple


__all__ = ['Convent', 'ConventAuthorization']


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


class ConventAuthorizationType(NamedTuple):
    """Convent authorizations."""

    convent: Convent
    vote: bool


class ConventAuthorization(Enum):
    """Available convent authorizations."""

    AHC = ConventAuthorizationType(Convent.AHC, False)
    AHC_VOTE = ConventAuthorizationType(Convent.AHC, True)
    CC = ConventAuthorizationType(Convent.CC, False)
    CC_VOTE = ConventAuthorizationType(Convent.CC, True)
    FC = ConventAuthorizationType(Convent.FC, False)
    FC_VOTE = ConventAuthorizationType(Convent.FC, True)
    FCC = ConventAuthorizationType(Convent.FCC, False)
    FCC_VOTE = ConventAuthorizationType(Convent.FCC, True)

    def __getattr__(self, attribute: str) -> Any:
        return getattr(self.value, attribute)
