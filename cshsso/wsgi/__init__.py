"""Core WSGI interface for session and user handling."""

from cshsso.application import Application
from cshsso.wsgi.account import show as show_account
from cshsso.wsgi.account import patch as patch_account
from cshsso.wsgi.account import delete as delete_account
from cshsso.wsgi.account import set_status
from cshsso.wsgi.account import set_commissions
from cshsso.wsgi.login import login
from cshsso.wsgi.logout import logout
from cshsso.wsgi.register import register, confirm_registration
from cshsso.wsgi.roles import list_circles
from cshsso.wsgi.roles import list_commissions
from cshsso.wsgi.roles import list_commission_groups
from cshsso.wsgi.roles import list_status


__all__ = ['APPLICATION']


APPLICATION = Application('CSHSSO')
APPLICATION.route('/login', methods=['POST'])(login)
APPLICATION.route('/logout', methods=['POST'])(logout)
APPLICATION.route('/register', methods=['POST'])(register)
APPLICATION.route('/register/confirm', methods=['POST'])(confirm_registration)
APPLICATION.route('/account', methods=['GET'])(show_account)
APPLICATION.route('/account', methods=['PATCH'])(patch_account)
APPLICATION.route('/account/delete', methods=['POST'])(delete_account)
APPLICATION.route('/account/status', methods=['POST'])(set_status)
APPLICATION.route('/account/commissions', methods=['POST'])(
    set_commissions)
APPLICATION.route('/roles/circles', methods=['GET'])(list_circles)
APPLICATION.route('/roles/commissions', methods=['GET'])(list_commissions)
APPLICATION.route('/roles/commission-groups', methods=['GET'])(
    list_commission_groups)
APPLICATION.route('/roles/status', methods=['GET'])(list_status)
