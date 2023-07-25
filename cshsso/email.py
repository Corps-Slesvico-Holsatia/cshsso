"""Sending emails."""

from functools import cache
from typing import Iterable

from emaillib import EMail, Mailer

from cshsso.config import CONFIG


__all__ = ["send"]


@cache
def get_mailer(*, section: str = "email") -> Mailer:
    """Returns the mailer as per the configuration."""

    return Mailer(
        CONFIG.get(section, "server"),
        CONFIG.getint(section, "port"),
        CONFIG.get(section, "login"),
        CONFIG.get(section, "passwd"),
    )


def send(emails: Iterable[EMail]) -> None:
    """Sends the provided emails."""

    return get_mailer().send(emails)
