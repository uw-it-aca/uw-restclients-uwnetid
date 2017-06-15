import logging
import os
from os.path import abspath, dirname
from restclients_core.dao import DAO


class UWNetID_DAO(DAO):
    def service_name(self):
        return 'nws'

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]
