"""
Interface for interacting with the UWNetID Subscription Web Service.
"""

from datetime import datetime
import logging
import json
from uw_uwnetid.models import UwEmailForwarding, Subscription
from uw_uwnetid.subscription import get_netid_subscriptions,\
    select_subscription


logger = logging.getLogger(__name__)
subs_code = Subscription.SUBS_CODE_U_FORWARDING


def get_email_forwarding(netid):
    """
    Return a restclients.models.uwnetid.UwEmailForwarding object
    on the given uwnetid
    """
    return get_uwemail_forwarding(select_uforwarding(
        get_netid_subscriptions(netid, subs_code)))


def select_uforwarding(subs):
    return select_subscription(subs_code, subs)


def get_uwemail_forwarding(subscription):
    return_obj = UwEmailForwarding()
    if subscription.data_value:
        return_obj.fwd = subscription.data_value
    return_obj.permitted = subscription.permitted
    return_obj.status = subscription.status_name
    return return_obj
