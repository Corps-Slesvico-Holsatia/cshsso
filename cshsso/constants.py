"""Common hard-coded constants."""

__all__ = [
    'SESSION_ID',
    'SESSION_SECRET',
    'USER_ID',
    'PW_RESET_TEXT',
    'PW_RESET_URL'
]


SESSION_ID = 'cshsso-session-id'
SESSION_SECRET = 'cshsso-session-secret'
USER_ID = 'cshsso-user-id'
PW_RESET_TEXT = '''Sehr geehrter Nutzer,

bitte folgen Sie dem unten stehenden Link um
Ihr Password zurückzusetzen.

{}

Mit freundlichen Grüßen

Der CC der Slesvico-Holsatia
'''
PW_RESET_URL = 'https://cshsso.slesvico-holsatia.org/pwreset/confirm?token={}'
