# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from datetime import date
from unittest import TestCase
from uw_uwnetid.models import Subscription
from uw_uwnetid.subscription_105 import get_email_forwarding
from restclients_core.exceptions import DataFailureException
from uw_uwnetid.util import fdao_uwnetid_override


@fdao_uwnetid_override
class EmailForwardingTest(TestCase):

    def test_get_email_forwarding(self):
        uw_email = get_email_forwarding("javerage")
        self.assertEqual(uw_email.status, "Active")
        self.assertTrue(uw_email.is_active())
        self.assertTrue(uw_email.permitted)
        self.assertFalse(uw_email.is_uwgmail())
        self.assertTrue(uw_email.is_uwlive())
        self.assertEqual(uw_email.fwd, "javerage@ol.uw.edu")

        uw_email = get_email_forwarding("none")
        self.assertTrue(uw_email.permitted)
        self.assertEqual(uw_email.status, "Inactive")
        self.assertIsNone(uw_email.fwd)
        self.assertFalse(uw_email.is_active())
        self.assertFalse(uw_email.is_uwgmail())
        self.assertFalse(uw_email.is_uwlive())

        uw_email = get_email_forwarding("jbothell")
        self.assertEqual(uw_email.status, "Active")
        self.assertEqual(uw_email.fwd, "jbothell@gamail.uw.edu")
        self.assertTrue(uw_email.is_active())
        self.assertTrue(uw_email.permitted)
        self.assertTrue(uw_email.is_uwgmail())
        self.assertFalse(uw_email.is_uwlive())

        uw_email = get_email_forwarding("eight")
        self.assertEqual(uw_email.status, "Active")
        self.assertEqual(uw_email.fwd, "eight@ol.uw.edu")
        self.assertTrue(uw_email.is_active())
        self.assertTrue(uw_email.permitted)
        self.assertFalse(uw_email.is_uwgmail())
        self.assertTrue(uw_email.is_uwlive())

    def test_invalid_user(self):
        # Testing error message in a 200 response
        self.assertRaises(DataFailureException,
                          get_email_forwarding,
                          "invalidnetid")
        # Testing non-200 response
        self.assertRaises(DataFailureException,
                          get_email_forwarding,
                          "invalidnetid123")

        try:
            get_email_forwarding("invalidnetid")
        except DataFailureException as ex:
            self.assertEqual(ex.msg, "No such NetID 'invalidnetid'")
