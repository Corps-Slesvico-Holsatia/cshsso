"""Modify user commissions."""

from flask import request, Response

from cshsso.decorators import authenticated
from cshsso.localproxies import USER
from cshsso.orm import User
from cshsso.ormfuncs import get_user, pass_commission as _pass_commission
from cshsso.roles import Commission


___all__ = ['pass_commission']


@authenticated
def pass_commission() -> Response:
    """Pass a commission to another user."""

    try:
        commission = Commission.from_string(request.json['commission'])
    except KeyError:
        return ('No commission specified.', 400)
    except ValueError:
        return ('No such commission.', 404)

    try:
        dst = get_user(request.json['user'])
    except KeyError:
        return ('No user specified.', 400)
    except (TypeError, ValueError):
        return ('User ID must be an int.', 400)
    except User.DoesNotExist:
        return ('No such user.', 404)

    _pass_commission(commission, USER, dst)
    return ('Commission passed.', 200)
