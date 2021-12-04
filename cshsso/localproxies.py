"""Local proxies."""

from functools import partial

from werkzeug.local import LocalProxy

from cshsso.orm.functions import get_current_user
from cshsso.session import get_session


__all__ = ['SESSION', 'USER']


class ModelProxy(LocalProxy):
    """Extended local proxy for database models."""

    def __enter__(self):
        return self._get_current_object()

    def __exit__(self, typ, value, traceback):
        pass

    def __int__(self) -> int:
        return self._get_current_object()._pk


SESSION = ModelProxy(get_session)
USER = ModelProxy(partial(get_current_user, SESSION))
