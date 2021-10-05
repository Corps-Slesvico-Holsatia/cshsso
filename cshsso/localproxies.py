"""Local proxies."""

from werkzeug.local import LocalProxy

from cshsso.session import get_session


__all__ = ['SESSION', 'USER']


SESSION = LocalProxy(get_session)
USER = LocalProxy(lambda: SESSION.user)
