"""Common hard-coded constants."""

from datetime import timedelta

__all__ = [
    "PW_RESET_TEXT",
    "PW_RESET_TOKEN_VALIDITY",
    "SESSION_ID",
    "SESSION_SECRET",
    "SESSION_VALIDITY",
    "USER_ID",
]


# TODO: Outsource to config file.
PW_RESET_TEXT = """Sehr geehrter Nutzer,

bitte folgen Sie dem unten stehenden Link um
Ihr Password zurückzusetzen.

{}

Mit freundlichen Grüßen

Der CC der Slesvico-Holsatia
"""
PW_RESET_TOKEN_VALIDITY = timedelta(days=1)
SESSION_ID = "cshsso-session-id"
SESSION_SECRET = "cshsso-session-secret"
SESSION_VALIDITY = timedelta(weeks=1)
USER_ID = "cshsso-user-id"
