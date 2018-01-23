"""
Interface for interacting with the UWNetID Subscription Web Service.
"""

from datetime import datetime
import logging
import json
from uw_uwnetid.models import UwEmailForwarding, \
    Subscription, SubscriptionAction, SubscriptionPermit
from uw_uwnetid import get_resource, post_resource


logger = logging.getLogger(__name__)


def get_email_forwarding(netid):
    """
    deprecated: use subscription_105.get_email_forwarding
    """
    subscriptions = get_netid_subscriptions(netid,
                                            Subscription.
                                            SUBS_CODE_U_FORWARDING)
    for subscription in subscriptions:
        if (subscription.subscription_code == Subscription.
                SUBS_CODE_U_FORWARDING):
            return_obj = UwEmailForwarding()
            if subscription.data_value:
                return_obj.fwd = subscription.data_value
            return_obj.permitted = subscription.permitted
            return_obj.status = subscription.status_name
            return return_obj

    return None


def get_netid_subscriptions(netid, subscription_codes):
    """
    Returns a list of uwnetid.subscription objects
    corresponding to the netid and subscription code or list provided
    """
    url = _netid_subscription_url(netid, subscription_codes)
    response = get_resource(url)
    return _json_to_subscriptions(response)


def select_subscription(subs_code, subscriptions):
    """
    Return the uwnetid.subscription object with the subs_code.
    """
    if subs_code and subscriptions:
        for subs in subscriptions:
            if (subs.subscription_code == subs_code):
                return subs
    return None


def modify_subscription_status(netid, subscription_code, status):
    """
    Post a subscription 'modify' action for the given netid
    and subscription_code
    """
    url = _netid_subscription_url(netid, subscription_code)
    body = {
        'action': 'modify',
        'value': str(status)
    }

    response = post_resource(url, json.dumps(body))
    return _json_to_subscriptions(response)


def update_subscription(netid, action, subscription_code, data_field=None):
    """
    Post a subscription action for the given netid and subscription_code
    """
    url = '/nws/v1/subscription.json'
    action = {
        'uwNetID': netid,
        'action': action,
        'subscriptionCode': str(subscription_code)
    }

    if isinstance(data_field, tuple) and len(data_field) == 2:
        action[data_field[0]] = str(data_field[1])

    body = {'actionList': [action]}
    response = post_resource(url, json.dumps(body))
    return _json_to_subscriptions(response)


def _netid_subscription_url(netid, subscription_codes):
    """
    Return UWNetId resource for provided netid and subscription
    code or code list
    """
    return "/nws/v1/uwnetid/%s/subscription/%s" % (
        netid, (','.join([str(n) for n in subscription_codes])
                if isinstance(subscription_codes, (list, tuple))
                else subscription_codes))


def _json_to_subscriptions(response_body):
    """
    Returns a list of Subscription objects
    """
    data = json.loads(response_body)
    subscriptions = []
    for subscription_data in data.get("subscriptionList", []):
        subscriptions.append(Subscription().from_json(
            data.get('uwNetID'), subscription_data))

    return subscriptions
