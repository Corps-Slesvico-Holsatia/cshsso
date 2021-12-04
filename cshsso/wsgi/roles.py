"""Lising of static roles information."""

from wsgilib import JSON

from cshsso.roles import Circle, Commission, CommissionGroup, Status


__all__ = [
    'list_status',
    'list_circles',
    'list_commissions',
    'list_commission_groups'
]


def list_status() -> JSON:
    """Lists available status."""

    return JSON([status.to_json() for status in Status])


def list_circles() -> JSON:
    """Lists available circles."""

    return JSON([{
        'name': circle.name,
        'status': [status.to_json() for status in circle]
    } for circle in Circle])


def list_commissions() -> JSON:
    """Lists available commissions."""

    return JSON([commission.to_json() for commission in Commission])


def list_commission_groups() -> JSON:
    """Lists available commission groups."""

    return JSON([{
        'name': cgroup.name,
        'status': [status.to_json() for status in cgroup]
    } for cgroup in CommissionGroup])
