"""
Interface for interacting with the UWNetID Subscription Web Service.
"""

from uw_uwnetid.models import SubscriptionPermit, Subscription
from uw_uwnetid.subscription import get_netid_subscriptions


subs_code = Subscription.SUBS_CODE_KERBEROS


def get_kerberos_subs(netid):
    """
    Return a Subscription object on the given uwnetid
    """
    return select_kerberos(get_netid_subscriptions(netid, subs_code))


def select_kerberos(subs):
    if subs is not None:
        for subscription in subs:
            if (subscription.subscription_code ==
                    Subscription.SUBS_CODE_KERBEROS):
                return subscription
    return None


def get_kerberos_subs_permits(netid):
    """
    Return a list of restclients.models.uwnetid.SubscriptionPermit objects
    on the given uwnetid
    """
    subs = get_kerberos_subs(netid)
    if subs is not None:
        return subs.permits
    return None


def is_current_staff(netid):
    return has_staff_in_permits(get_kerberos_subs_permits(netid))


def has_staff_in_permits(permits):
    if permits is None:
        return False
    for permit in permits:
        if permit.is_category_staff() and permit.is_status_current():
            return True
    return False


def is_current_faculty(netid):
    return has_faculty_in_permits(get_kerberos_subs_permits(netid))


def has_faculty_in_permits(permits):
    if permits is None:
        return False
    for permit in permits:
        if permit.is_category_faculty() and permit.is_status_current():
            return True
    return False


def is_current_clinician(netid):
    return has_clinician_in_permits(get_kerberos_subs_permits(netid))


def has_clinician_in_permits(permits):
    if permits is None:
        return False
    for permit in permits:
        if permit.is_status_current() and\
                (permit.is_category_clinician() or
                 permit.is_category_clinician_netid_only()):
            return True
    return False
