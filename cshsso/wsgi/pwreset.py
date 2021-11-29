"""Password reset."""

from typing import Union
from uuid import UUID

from flask import request, Response

from emaillib import EMail
from peeweeplus import PasswordTooShort
from recaptcha import recaptcha

from cshsso.config import CONFIG
from cshsso.email import send
from cshsso.orm import PasswordResetToken, User


__all__ = ['request_pw_reset', 'confirm_pw_reset']


EMAIL_TEXT = '''Sehr geehrter Nutzer,

bitte folgen Sie dem unten stehenden Link um
Ihr Password zurückzusetzen.

{}

Mit freundlichen Grüßen

Der CC der Slesvico-Holsatia
'''
RESET_URL = 'https://cshsso.slesvico-holsatia.org/pwreset/confirm?token={}'


def password_reset_pending(user: Union[User, int]) -> bool:
    """Checks whether a password request is
    already pending for the given user.
    """

    result = False

    for pw_reset_token in PasswordResetToken.select().where(
                PasswordResetToken.user == user):
        if pw_reset_token.is_valid():
            result = True
        else:
            pw_reset_token.delete_instance()

    return result


def get_email(password_reset_token: str, email_address: str, *,
              section: str = 'pwreset') -> EMail:
    """Returns an email object."""

    return EMail(
        CONFIG.get(section, 'subject',
                   fallback='Zurücklsetzen Ihres Passworts'),
        CONFIG.get(section, 'sender',
                   fallback='noreply@cshsso.slesvico-holsatia.org'),
        email_address,
        plain=CONFIG.get(section, 'template', fallback=EMAIL_TEXT).format(
            CONFIG.get(section, 'url', fallback=RESET_URL).format(
                password_reset_token
            )
        )
    )


@recaptcha(CONFIG)
def request_pw_reset() -> Response:
    """Requests a password reset."""

    if not (email := request.json.get('email')):
        return ('No email address specified.', 400)

    try:
        user = User.select().where(User.email == email).get()
    except User.DoesNotExist:
        return ('Reset request successful.', 200)   # Mitigate sniffing.

    if password_reset_pending(user):
        return ('You already requested a password reset.', 400)

    password_reset_token = PasswordResetToken(user=user)
    password_reset_token.save()

    if send([get_email(password_reset_token.token.hex, user.email)]):
        return ('Reset request successful.', 200)

    return ('Could not email reset token.', 500)


@recaptcha(CONFIG)
def confirm_pw_reset() -> Response:
    """Resets the user's password."""

    try:
        token = UUID(request.json.get('token'))
    except (TypeError, ValueError):
        return ('Invalid token.', 400)

    try:
        password_reset_token = PasswordResetToken.select(
            PasswordResetToken, User).join(User).where(
            PasswordResetToken.token == token).get()
    except PasswordResetToken.DoesNotExist:
        return ('Invalid token.', 400)

    if not password_reset_token.is_valid():
        return ('Invalid token.', 400)

    if not (password := request.json.get('passwd')):
        return ('No password specified.', 400)

    try:
        (user := password_reset_token.user).password = password
    except PasswordTooShort:
        return ('Password is too short.', 400)

    user.save()
    password_reset_token.delete_instance()
    return ('Password set.', 200)
