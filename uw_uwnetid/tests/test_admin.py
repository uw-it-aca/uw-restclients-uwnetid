from unittest import TestCase
from uw_uwnetid.admin import get_admins_for_shared_netid
from uw_uwnetid.util import fdao_uwnetid_override
from restclients_core.exceptions import DataFailureException


@fdao_uwnetid_override
class AdminListTest(TestCase):
    def test_get_admins_for_shared_netid(self):
        adminList = get_admins_for_shared_netid('emailinfo')
        self.assertEquals(len(adminList), 4)
        owner = 0
        admin = 0
        for admin in adminList:
            if admin.is_owner():
                owner += 1
            if admin.is_admin():
                admin += 1

        self.assertEquals(owner, 9)
        self.assertEquals(admin, 13)

    def test_no_admins_for_shared_netid(self):
        try:
            get_admins_for_shared_netid('foobar')
        except DataFailureException as ex:
            self.assertEquals(ex.status, 404)
