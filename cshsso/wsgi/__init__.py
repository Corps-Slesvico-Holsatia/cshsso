"""Core WSGI interface for session and user handling."""

from cshsso.application import Application
from cshsso.wsgi.login import login
from cshsso.wsgi.logout import logout
from cshsso.wsgi.register import register
from cshsso.wsgi.account import show as show_account
from cshsso.wsgi.account import patch as patch_account
from cshsso.wsgi.account import delete as delete_account
from cshsso.wsgi.account import set_status
from cshsso.wsgi.account import set_commissions


__all__ = ['APPLICATION']


APPLICATION = Application('CSHSSO')
APPLICATION.route('/login', methods=['POST'])(login)
APPLICATION.route('/logout', methods=['POST'])(logout)
APPLICATION.route('/register', methods=['POST'])(register)
APPLICATION.route('/account', methods=['GET'])(show_account)
APPLICATION.route('/account', methods=['PATCH'])(patch_account)
APPLICATION.route('/account/delete', methods=['POST'])(delete_account)
APPLICATION.route('/account/status', methods=['POST'])(set_status)
APPLICATION.route('/account/commissions', methods=['POST'])(
    set_commissions)
