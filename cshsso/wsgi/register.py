"""User registration."""

from flask import request
from peewee import IntegrityError

from emaillib import EMail
from recaptcha import recaptcha
from wsgilib import JSONMessage

from cshsso.config import CONFIG
from cshsso.decorators import authenticated, Authorization
from cshsso.email import send
from cshsso.orm.models import User
from cshsso.roles import Status


__all__ = ["register", "confirm_registration"]


def user_from_json(json: dict) -> User:
    """Creates a new user from a dict."""

    return User(
        email=json["email"],
        passwd=json["passwd"],
        first_name=json["first_name"],
        last_name=json["last_name"],
        status=Status[json["status"]],
    )


def get_email(user: User, *, section: str = "registration") -> EMail:
    """Returns a registration email for the given user."""

    return EMail(
        CONFIG.get(section, "subject"),
        CONFIG.get(section, "sender"),
        user.email,
        plain=CONFIG.get(section, "template").format(user),
    )


@recaptcha(
    lambda: CONFIG["recaptcha"],
    lambda: request.json.pop("response"),
    lambda: request.remote_addr,
)
def register() -> JSONMessage:
    """Registers a new user."""

    try:
        user = user_from_json(request.json)
    except KeyError as error:
        return JSONMessage(str(error), status=400)

    try:
        user.save()
    except ValueError:
        return JSONMessage("Invalid value(s) provided.", status=400)
    except IntegrityError:
        return JSONMessage("User already exists.", status=400)

    send([get_email(user)])
    return JSONMessage("User added.", id=user.id, status=201)


@authenticated
@Authorization.CHARGES
def confirm_registration() -> JSONMessage:
    """Confirms a registration."""

    if not (user_id := request.json.get("user")):
        return JSONMessage("No user ID specified.", status=400)

    try:
        user = User.select().where(User.id == user_id).get()
    except ValueError:
        return JSONMessage("Invalid user ID.", status=400)
    except User.DoesNotExist:
        return JSONMessage("No such user.", status=404)

    user.verified = True
    user.save()
    return JSONMessage("User verified.", status=200)
