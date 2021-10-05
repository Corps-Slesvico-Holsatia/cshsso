"""Core WSGI interface for session and user handling."""

from cshsso.application import Application
from cshsso.wsgi.login import login
from cshsso.wsgi.logout import logout
from cshsso.wsgi.register import register


__all__ = ['APPLICATION']


APPLICATION = Application('CSHSSO')
APPLICATION.route('/login', methods=['POST'])(login)
APPLICATION.route('/logout', methods=['POST'])(logout)
APPLICATION.route('/register', methods=['POST'])(register)
