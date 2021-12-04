"""Password reset."""

from typing import Union
from uuid import UUID

from flask import request

from emaillib import EMail
from peeweeplus import PasswordTooShort
from recaptcha import recaptcha
from wsgilib import JSONMessage

from cshsso.config import CONFIG
from cshsso.constants import PW_RESET_TEXT
from cshsso.email import send
from cshsso.orm import PasswordResetToken, User


__all__ = ['request_pw_reset', 'confirm_pw_reset']


INVALID_TOKEN = JSONMessage('Invalid token.', status=400)
RESET_SUCCEEDED = JSONMessage('Reset request successful.', status=200)


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


def get_email(password_reset_token: str, email_address: str, url: str, *,
              section: str = 'pwreset') -> EMail:
    """Returns an email object."""

    return EMail(
        CONFIG.get(section, 'subject',
                   fallback='Zurücklsetzen Ihres Passworts'),
        CONFIG.get(section, 'sender',
                   fallback='noreply@cshsso.slesvico-holsatia.org'),
        email_address,
        plain=CONFIG.get(section, 'template', fallback=PW_RESET_TEXT).format(
            url.format(password_reset_token)
        )
    )


@recaptcha(CONFIG)
def request_pw_reset() -> JSONMessage:
    """Requests a password reset."""

    if not (email := request.json.get('email')):
        return JSONMessage('No email address specified.', status=400)

    if not (url := request.json.get('url')):
        return JSONMessage('No URL specified.', status=400)

    try:
        user = User.select().where(User.email == email).get()
    except User.DoesNotExist:
        # Mitigate sniffing.
        return RESET_SUCCEEDED

    if password_reset_pending(user):
        return JSONMessage('You already requested a password reset.',
                           status=400)

    password_reset_token = PasswordResetToken(user=user)
    password_reset_token.save()

    if send([get_email(password_reset_token.token.hex, user.email, url)]):
        return RESET_SUCCEEDED

    return JSONMessage('Could not email reset token.', status=500)


@recaptcha(CONFIG)
def confirm_pw_reset() -> JSONMessage:
    """Resets the user's password."""

    try:
        token = UUID(request.json.get('token'))
    except (TypeError, ValueError):
        return INVALID_TOKEN

    try:
        password_reset_token = PasswordResetToken.select(
            PasswordResetToken, User).join(User).where(
            PasswordResetToken.token == token).get()
    except PasswordResetToken.DoesNotExist:
        return INVALID_TOKEN

    if not password_reset_token.is_valid():
        password_reset_token.delete_instance()
        return INVALID_TOKEN

    if not (password := request.json.get('passwd')):
        return JSONMessage('No password specified.', status=400)

    try:
        (user := password_reset_token.user).password = password
    except PasswordTooShort:
        return JSONMessage('Password is too short.', status=400)

    user.save()
    password_reset_token.delete_instance()
    return JSONMessage('Password set.', status=200)
