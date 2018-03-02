"""
This is the interface for interacting with
the uwnetid subscription web service.
"""

import logging
import json
from commonconf import settings
from restclients_core.exceptions import DataFailureException
from uw_uwnetid.dao import UWNetID_DAO


INVALID_USER_MSG = "No such NetID"
DAO = UWNetID_DAO()
logger = logging.getLogger(__name__)


def url_version():
    return '/nws/%s' % (
        getattr(settings, 'RESTCLIENTS_UWNETID_VERSION', 'v1'))


def url_base():
    return '%s/uwnetid' % (url_version())


def get_resource(url):
    response = DAO.getURL(url, {'Accept': 'application/json'})
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
    response = DAO.postURL(url, {
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
