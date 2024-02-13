# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from restclients_core.exceptions import DataFailureException
from uw_uwnetid.subscription_64 import get_2fa_subs
from uw_uwnetid.util import fdao_uwnetid_override


@fdao_uwnetid_override
class DuoTwoFactorSubsTest(TestCase):

    def test_get_2fa_subs(self):
        subs = get_2fa_subs("bill")
        self.assertIsNotNone(subs.json_data())
        self.assertTrue(subs.is_status_active())
        self.assertEqual(subs.status_name, 'Active')
        self.assertEqual(subs.subscription_name,
                         'Duo Two-Factor Authentication')
        self.assertTrue(subs.permitted)
        self.assertEqual(len(subs.actions), 1)
        self.assertEqual(len(subs.permits), 1)
        self.assertEqual(subs.permits[0].category_code, 4)
        self.assertEqual(subs.permits[0].status_name, 'current')

        subs = get_2fa_subs("javerage")
        self.assertTrue(subs.is_status_active())
        self.assertEqual(subs.status_code, 20)
        self.assertEqual(subs.subscription_name,
                         'Duo Two-Factor Authentication')
        self.assertTrue(subs.permitted)
        self.assertEqual(len(subs.actions), 1)
        self.assertEqual(len(subs.permits), 1)
        self.assertEqual(subs.permits[0].category_code, 14)
        self.assertEqual(subs.permits[0].status_name, 'current')

        subs = get_2fa_subs("none")
        self.assertFalse(subs.is_status_active())

        self.assertRaises(DataFailureException,
                          get_2fa_subs,
                          "error")
