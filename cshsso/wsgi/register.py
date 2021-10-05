"""User registration."""

from flask import request, Response
from peewee import IntegrityError
from recaptcha import recaptcha

from cshsso.config import CONFIG
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

    return ('User added.', 201)
