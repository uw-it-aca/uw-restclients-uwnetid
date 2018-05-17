"""
Interface for interacting with the UWNetID Web Service Supported resource.
"""

import logging
import json
from uw_uwnetid.models import Supported
from uw_uwnetid import url_base, get_resource


logger = logging.getLogger(__name__)


def get_supported_resources(netid):
    """
    Returns list of Supported resources
    """
    url = _netid_supported_url(netid)
    response = get_resource(url)
    return _json_to_supported(response)


def _netid_supported_url(netid):
    """
    Return UWNetId resource for provided netid supported
    resources
    """
    return "%s/%s/supported.json" % (url_base(), netid)


def _json_to_supported(response_body):
    """
    Returns a list of Supported objects
    """
    data = json.loads(response_body)
    supported = []
    for supported_data in data.get("supportedList", []):
        supported.append(Supported().from_json(
            supported_data))

    return supported
