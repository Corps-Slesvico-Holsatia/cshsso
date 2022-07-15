"""Semester handling."""
# pylint: disable=W0621

from __future__ import annotations
from datetime import date, datetime
from enum import Enum
from typing import NamedTuple


__all__ = ['SemesterType', 'Semester']


class SemesterType(str, Enum):
    """Type of semester."""

    WS = 'Wintersemester'
    SS = 'Sommersemester'


class Semester(NamedTuple):
    """A semester."""

    type: SemesterType
    years: list[int]

    @classmethod
    def from_date(cls, date: date, *, summer_begin: int = 4,
                  winter_begin: int = 10) -> Semester:
        """Creates a semester from the given date."""
        if summer_begin <= date.month < winter_begin:
            return cls(SemesterType.SS, [date.year])

        if date.month < summer_begin:
            return cls(SemesterType.WS, [date.year - 1, date.year])

        return cls(SemesterType.WS, [date.year, date.year + 1])

    @classmethod
    def from_datetime(cls, datetime: datetime, **kwargs) -> Semester:
        """Creates a semester from the given datetime."""
        return cls.from_date(datetime.date(), **kwargs)

    @classmethod
    def now(cls, **kwargs) -> Semester:
        """Returns the current semester."""
        return cls.from_date(date.today(), **kwargs)

    def next(self) -> Semester:
        """Returns the next semester."""
        if self.type == SemesterType.WS:
            return Semester(SemesterType.SS, [self.years[1]])

        return Semester(SemesterType.WS, [year := self.years[0], year + 1])

    def previous(self) -> Semester:
        """Returns the previous semester."""
        if self.type == SemesterType.WS:
            return Semester(SemesterType.SS, [self.years[0]])

        return Semester(SemesterType.WS, [self.years[0] - 1, self.years[0]])
