"""
Interface for interacting with the UWNetID Subscription 64
"""

from uw_uwnetid.models import Subscription
from uw_uwnetid.subscription import get_netid_subscriptions


subs_code = Subscription.SUBS_CODE_2FA


def get_2fa_subs(netid):
    """
    Return a Subscription object on the given uwnetid
    """
    subs = get_netid_subscriptions(netid, subs_code)
    if subs is not None:
        for subscription in subs:
            if subscription.subscription_code == subs_code:
                return subscription
    return None
