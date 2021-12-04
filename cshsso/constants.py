"""Common hard-coded constants."""

from datetime import timedelta

__all__ = [
    'EMAIL_REGEX',
    'NAME_REGEX',
    'PW_RESET_TEXT',
    'PW_RESET_TOKEN_VALIDITY',
    'SESSION_ID',
    'SESSION_SECRET',
    'SESSION_VALIDITY',
    'USER_ID'
]


# Taken from: https://stackoverflow.com/a/201378/3515670
EMAIL_REGEX = (
    r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/='''
    r'''?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]'''
    r'''|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*'''
    r'''[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|'''
    r'''[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|'''
    r'''1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c'''
    r'''\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''
)
NAME_REGEX = r'''^[A-Za-zÄäÖöÜüß '-]+$'''
PW_RESET_TEXT = '''Sehr geehrter Nutzer,

bitte folgen Sie dem unten stehenden Link um
Ihr Password zurückzusetzen.

{}

Mit freundlichen Grüßen

Der CC der Slesvico-Holsatia
'''
PW_RESET_TOKEN_VALIDITY = timedelta(days=1)
SESSION_ID = 'cshsso-session-id'
SESSION_SECRET = 'cshsso-session-secret'
SESSION_VALIDITY = timedelta(weeks=1)
USER_ID = 'cshsso-user-id'
