"""User registration."""

from flask import request, Response, jsonify
from peewee import IntegrityError

from emaillib import EMail
from recaptcha import recaptcha

from cshsso.config import CONFIG
from cshsso.email import send
from cshsso.orm import User
from cshsso.roles import Status


__all__ = ['register']


def user_from_json(json: dict) -> User:
    """Creates a new user from a dict."""

    return User(
        email=json['email'],
        passwd=json['passwd'],
        first_name=json['first_name'],
        last_name=json['last_name'],
        status=Status[json['status']]
    )


def get_email(user: User, *, section: str = 'registration') -> EMail:
    """Returns a registration email for the given user."""

    return EMail(
        CONFIG.get(section, 'subject'), CONFIG.get(section, 'sender'),
        user.email, plain=CONFIG.get(section, 'template').format(user)
    )


@recaptcha(CONFIG)
def register() -> Response:
    """Registers a new user."""

    try:
        user = user_from_json(request.json)
    except KeyError as error:
        return (str(error), 400)

    try:
        user.save()
    except ValueError:
        return ('Invalid value(s) provided.', 400)
    except IntegrityError:
        return ('Email address already taken.', 400)

    sent = send([get_email(user)])
    return (jsonify(message='User added.', email_sent=sent, id=user.id), 201)
