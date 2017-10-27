from datetime import date
from unittest import TestCase
from uw_uwnetid.models import UwPassword, convert_seconds_to_days,\
    convert_days_to_seconds
from uw_uwnetid.password import get_uwnetid_password
from restclients_core.exceptions import DataFailureException
from uw_uwnetid.util import fdao_uwnetid_override


@fdao_uwnetid_override
class UwPasswordTest(TestCase):

    def test_status(self):
        pw = UwPassword(uwnetid='userid',
                        kerb_status="Active",
                        last_change=None,
                        last_change_med=None,
                        expires_med=None,
                        interval_med=None,
                        minimum_length=8,
                        time_stamp=None)
        self.assertFalse(pw.is_status_active())
        self.assertFalse(pw.is_status_person())
        self.assertFalse(pw.is_active_person())
        pw.netid_status = ["Person", "Active"]
        self.assertEquals(pw.netid_status[0], "Person")
        self.assertEquals(pw.netid_status[1], "Active")
        self.assertTrue(pw.is_status_active())
        self.assertTrue(pw.is_status_person())
        self.assertTrue(pw.is_active_person())

        self.assertTrue(pw.is_kerb_status_active())
        self.assertFalse(pw.is_kerb_status_disabled())
        self.assertFalse(pw.is_kerb_status_expired())
        self.assertFalse(pw.is_kerb_status_inactive())
        self.assertFalse(pw.is_kerb_status_other())
        self.assertFalse(pw.is_kerb_status_pending())
        self.assertFalse(pw.is_kerb_status_suspended())

        pw.kerb_status = "Disabled"
        self.assertTrue(pw.is_kerb_status_disabled())
        pw.kerb_status = "Expired"
        self.assertTrue(pw.is_kerb_status_expired())
        pw.kerb_status = "Inactive"
        self.assertTrue(pw.is_kerb_status_inactive())
        pw.kerb_status = "Pending"
        self.assertTrue(pw.is_kerb_status_pending())
        pw.kerb_status = "Other"
        self.assertTrue(pw.is_kerb_status_other())
        pw.kerb_status = "Suspended"
        self.assertTrue(pw.is_kerb_status_suspended())

    def test_get_uwnetid_password(self):
        pw = get_uwnetid_password("javerage")
        self.assertEquals(len(pw.netid_status), 2)
        self.assertEquals(pw.netid_status[0], "Person")
        self.assertEquals(pw.netid_status[1], "Active")
        self.assertTrue(pw.is_active_person())
        self.assertTrue(pw.is_kerb_status_active())
        self.assertEqual(str(pw.last_change), '2015-01-27 10:49:42-08:00')
        self.assertEqual(str(pw.time_stamp), '2016-12-16 14:21:40-08:00')
        self.assertEqual(str(pw.time_stamp,), '2016-12-16 14:21:40-08:00')
        self.assertEqual(convert_seconds_to_days(pw.interval), 120)
        self.assertEqual(pw.minimum_length, 8)

        pw = get_uwnetid_password("bill")
        self.assertEquals(len(pw.netid_status), 2)
        self.assertTrue(pw.is_kerb_status_active())
        self.assertEqual(str(pw.last_change), '2016-10-13 10:33:52-07:00')
        self.assertEqual(str(pw.time_stamp), '2016-12-16 14:23:11-08:00')
        self.assertEqual(str(pw.expires_med), '2017-02-10 10:57:06-08:00')
        self.assertEqual(str(pw.last_change_med), '2016-10-13 10:57:06-07:00')
        self.assertEqual(convert_seconds_to_days(pw.interval_med), 120)
        self.assertEqual(pw.minimum_length, 8)

        self.assertEqual(
            convert_seconds_to_days(UwPassword.DEFAULT_MED_INTERVAL), 120)
