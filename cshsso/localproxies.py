"""Local proxies."""

from werkzeug.local import LocalProxy

from cshsso.session import get_session


__all__ = ['SESSION', 'ACCOUNT']


SESSION = LocalProxy(get_session)
ACCOUNT = LocalProxy(lambda: SESSION.account)
