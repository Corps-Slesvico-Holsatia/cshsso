"""Core WSGI interface for session and user handling."""

from cshsso.application import Application
from cshsso.wsgi.login import login


APPLICATION = Application('CSHSSO')
APPLICATION.route('/login', methods=['POST'], strict_slashes=False)(login)
