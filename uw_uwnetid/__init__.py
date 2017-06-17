"""
This is the interface for interacting with
the uwnetid subscription web service.
"""

import logging
import json
from uw_uwnetid.dao import UWNetID_DAO
from restclients_core.exceptions import DataFailureException


INVALID_USER_MSG = "No such NetID"
logger = logging.getLogger(__name__)


def get_resource(url):
    response = UWNetID_DAO().getURL(url, {'Accept': 'application/json'})
    logger.info("GET %s ==status==> %s" % (url, response.status))

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    # 'Bug' with lib API causing requests with no/invalid user to return a 200
    if INVALID_USER_MSG in response.data:
        json_data = json.loads(response.data)
        raise DataFailureException(url, 404, json_data["errorMessage"])

    logger.debug("GET %s ==data==> %s" % (url, response.data))

    return response.data


def post_resource(url, body):
    response = UWNetID_DAO().postURL(url, {
        'Content-Type': 'application/json',
        'Acept': 'application/json',
    }, body)
    logger.info("POST %s ==status==> %s" % (url, response.status))

    if response.status != 200:
        raise DataFailureException(url, response.status, response.data)

    # 'Bug' with lib API causing requests with no/invalid user to return a 200
    if INVALID_USER_MSG in response.data:
        json_data = json.loads(response.data)
        raise DataFailureException(url, 404, json_data["errorMessage"])

    logger.debug("POST %s ==data==> %s" % (url, response.data))

    return response.data
