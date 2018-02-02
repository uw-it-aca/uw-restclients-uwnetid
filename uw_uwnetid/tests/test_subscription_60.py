from unittest import TestCase
from uw_uwnetid.subscription_60 import get_kerberos_subs_permits,\
    is_current_undergrad, is_former_undergrad, is_current_student_employee,\
    is_current_grad, is_former_grad, is_former_student_employee,\
    is_current_staff, is_former_staff, get_kerberos_subs,\
    is_current_faculty, is_former_faculty, is_current_alumni,\
    is_current_clinician, is_former_clinician, is_current_retiree
from restclients_core.exceptions import DataFailureException
from uw_uwnetid.util import fdao_uwnetid_override


@fdao_uwnetid_override
class KerberosSubsTest(TestCase):

    def test_get_kerberos_subs_permits(self):
        permits = get_kerberos_subs_permits("javerage")
        self.assertFalse(is_current_staff(permits))
        self.assertTrue(is_current_alumni(permits))
        self.assertTrue(is_current_undergrad(permits))
        self.assertTrue(is_current_student_employee(permits))

        permits = get_kerberos_subs_permits("bill")
        self.assertTrue(is_current_staff(permits))
        self.assertTrue(is_former_grad(permits))
        self.assertTrue(is_former_student_employee(permits))
        self.assertFalse(is_current_faculty(permits))
        self.assertFalse(is_current_clinician(permits))

        permits = get_kerberos_subs_permits("phil")
        self.assertFalse(is_current_staff(permits))
        self.assertTrue(is_current_faculty(permits))
        self.assertTrue(is_current_alumni(permits))
        
        permits = get_kerberos_subs_permits("fred")
        self.assertTrue(is_current_clinician(permits))

        permits = get_kerberos_subs_permits("james")
        self.assertTrue(is_current_clinician(permits))

        subs = get_kerberos_subs("bill")
        self.assertTrue(subs.is_status_active())

        subs = get_kerberos_subs("phil")
        self.assertTrue(subs.is_status_active())

    def test_unpermitted(self):
        subs = get_kerberos_subs("none")
        self.assertFalse(subs.is_status_active())
        self.assertFalse(subs.is_status_inactive())
        self.assertFalse(subs.permitted)

    def test_expiring_subs(self):
        subs = get_kerberos_subs("eight")
        self.assertTrue(subs.is_status_active())
        self.assertFalse(subs.is_status_inactive())
        self.assertFalse(subs.permitted)

    def test_invalid_user(self):
        # Testing error message in a 200 response
        self.assertRaises(DataFailureException,
                          get_kerberos_subs,
                          "invalidnetid")
        # Testing non-200 response
        self.assertRaises(DataFailureException,
                          get_kerberos_subs,
                          "jnewstudent")
