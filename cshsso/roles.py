"""User roles."""

from __future__ import annotations
from contextlib import suppress
from enum import Enum
from typing import Iterator, NamedTuple, Optional


__all__ = ['RoleType', 'Status', 'Circle', 'Commission', 'CommissionGroup']


class RoleType(NamedTuple):
    """Status names."""

    name: str
    abbreviation: Optional[str] = None

    def __str__(self):
        return self.abbreviation or self.name

    def match(self, string: str) -> bool:
        """Matches a string."""
        return string in {self.name, self.abbreviation}

    def to_json(self) -> dict[str, str]:
        """Returns a JSON-ish dict."""
        return {'name': self.name, 'abbreviation': self.abbreviation}


class Status(Enum):
    """Member status."""

    # Members
    EB = RoleType('Ehrenbursche', 'EB')
    CB = RoleType('Corpsbursche', 'CB')
    IACB = RoleType('inaktiver Corpsbursche', 'iaCB')
    IACBOB = RoleType('inaktiver Corpsbursche ohne Band', 'iaCBoB')
    AH = RoleType('Alter Herr', 'AH')
    BBZ = RoleType('Burschenbierzipfler', 'BBZ')
    F = RoleType('Fuchs', 'F')
    FCK = RoleType('Fuchsenconkneipant', 'FCK')
    # Guests
    SPEF = RoleType('Spefuchs', 'Spef.')
    VG = RoleType('Verkehrsgast', 'VG')
    CORPSSCHWESTER = RoleType('Corpsschwester')
    FDC = RoleType('Freund des Corps', 'FdC')

    @classmethod
    def from_string(cls, string: str) -> Status:
        """Creates a Status element from a JSON string."""
        with suppress(KeyError):
            return cls[string]

        for status in cls:
            if status.value.match(string):
                return status

        raise ValueError(f'No status matching "{string}".')

    def to_json(self) -> dict[str, str]:
        """Returns a JSON-ish dict."""
        return self.value.to_json()


class Circle(Enum):
    """Corps circles."""

    INNER = {Status.EB, Status.CB, Status.IACB, Status.AH}
    OUTER = {Status.IACBOB, Status.BBZ, Status.F, Status.FCK}
    GUESTS = {Status.SPEF, Status.CORPSSCHWESTER, Status.FDC, Status.VG}

    def __contains__(self, value: Status) -> bool:
        return value in self.value

    def __iter__(self) -> Iterator[Status]:
        return iter(self.value)


class Commission(Enum):
    """Commission types."""

    # Chargen
    SENIOR = RoleType('Senior', 'xxx')
    CONSENIOR = RoleType('Consenior', 'xx')
    SUBSENIOR = RoleType('Subsenior', 'x')
    FM = RoleType('Fuchsmajor', 'FM')
    # Ämter
    KW = RoleType('CC-Kassenwart', 'KW')
    HW = RoleType('Hauswart', 'HW')
    GW = RoleType('Getränkewart', 'GW')
    KEILWART = RoleType('Keilwart')
    EDV = RoleType('EDV-Wart')
    # AHV
    AHV = RoleType('Altherrenvorstandsvorsitzender', 'AHV')
    AHV_STELLV = RoleType(
        'stellvertretender Altherrenvorstandsvorsitzender',
        'stellv. AHV'
    )
    AHKW = RoleType('Altherren-Kassenwart', 'AHKW')

    @classmethod
    def from_string(cls, string: str) -> Commission:
        """Creates a Commission element from a string."""
        with suppress(KeyError):
            return cls[string]

        for commission in cls:
            if commission.value.match(string):
                return commission

        raise ValueError(f'No commission matching "{string}".')

    def to_json(self) -> dict[str, str]:
        """Returns a JSON-ish dict."""
        return self.value.to_json()


class CommissionGroup(Enum):
    """Commission groups."""

    CHARGES = {Commission.SENIOR, Commission.CONSENIOR, Commission.SUBSENIOR,
               Commission.FM}
    COMMISSIONS = {Commission.KW, Commission.HW, Commission.GW,
                   Commission.KEILWART, Commission.EDV}
    AHV = {Commission.AHV, Commission.AHV_STELLV, Commission.AHKW}

    def __contains__(self, value: Commission) -> bool:
        return value in self.value

    def __iter__(self) -> Iterator[Commission]:
        return iter(self.value)
