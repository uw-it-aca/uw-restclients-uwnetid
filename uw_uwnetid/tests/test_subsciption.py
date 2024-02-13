# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from uw_uwnetid.models import Subscription
from uw_uwnetid.subscription_105 import get_uwemail_forwarding
from uw_uwnetid.subscription import (
    get_email_forwarding, get_netid_subscriptions,
    modify_subscription_status, update_subscription)
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
        self.assertEqual(uw_email.fwd,
                         "javerage@ol.uw.edu")

        uw_email = get_email_forwarding("none")
        self.assertTrue(uw_email.permitted)
        self.assertEqual(uw_email.status, "Inactive")
        self.assertIsNone(uw_email.fwd)
        self.assertFalse(uw_email.is_active())
        self.assertFalse(uw_email.is_uwgmail())
        self.assertFalse(uw_email.is_uwlive())

        uw_email = get_email_forwarding("jbothell")
        self.assertEqual(uw_email.status, "Active")
        self.assertEqual(uw_email.fwd,
                         "jbothell@gamail.uw.edu")
        self.assertTrue(uw_email.is_active())
        self.assertTrue(uw_email.permitted)
        self.assertTrue(uw_email.is_uwgmail())
        self.assertFalse(uw_email.is_uwlive())

        uw_email = get_email_forwarding("eight")
        self.assertEqual(uw_email.status, "Active")
        self.assertEqual(uw_email.fwd,
                         "eight@ol.uw.edu")
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


@fdao_uwnetid_override
class NetidSubscriptionTest(TestCase):

    def test_get_netid_subscriptions(self):
        subscriptions = get_netid_subscriptions('phil', [60, 64, 105])
        for subscription in subscriptions:
            if subscription.subscription_code == 105:
                self.assertEqual(subscription.data_value,
                                 'phil@gamail.uw.edu')
                email_forwarding = get_uwemail_forwarding(subscription)
                self.assertEqual(email_forwarding.fwd,
                                 'phil@gamail.uw.edu')

        subscriptions = get_netid_subscriptions(
            'javerage', [60, 20, 100, 105, 137, 41])
        self.assertEqual(len(subscriptions), 6)
        for subscription in subscriptions:
            if subscription.subscription_code == 60:
                self.assertEqual(subscription.status_code, 20)
                self.assertEqual(subscription.data_field, 'KPW')
                self.assertTrue(subscription.permitted)
                self.assertEqual(len(subscription.actions), 5)
                self.assertEqual(len(subscription.permits), 1)
                self.assertEqual(subscription.permits[0].category_code, 11)
                self.assertEqual(subscription.permits[0].status_name,
                                 'current')
            elif subscription.subscription_code == 20:
                self.assertTrue(subscription.permitted)
                self.assertEqual(len(subscription.actions), 6)
            elif subscription.subscription_code == 100:
                self.assertTrue(subscription.permitted)
            elif subscription.subscription_code == 105:
                self.assertTrue(subscription.permitted)
                self.assertEqual(len(subscription.actions), 7)
                self.assertEqual(subscription.data_field, 'FWD')
                self.assertEqual(subscription.data_value,
                                 'javerage@javerage.deskmail.washington.edu')
            elif subscription.subscription_code == 137:
                self.assertTrue(subscription.permitted)
                self.assertEqual(len(subscription.actions), 8)
                self.assertEqual(len(subscription.permits), 3)
                self.assertEqual(subscription.permits[0].category_code, 0)
                self.assertEqual(subscription.permits[0].data_value,
                                 'disk=1024')
                self.assertEqual(subscription.permits[1].status_code, 1)
                self.assertEqual(subscription.permits[1].data_value,
                                 'rate=4.17')
                self.assertEqual(subscription.permits[2].category_code, 11)
                self.assertEqual(subscription.permits[2].data_value,
                                 'max=1024.0 disk=1024.0')
            elif subscription.subscription_code == 41:
                self.assertFalse(subscription.permitted)


@fdao_uwnetid_override
class NetidPostSubscriptionTest(TestCase):
    def test_update_subscription(self):
        response_list = update_subscription('javerage', 'activate', 144)

        self.assertEqual(response_list[0].query['subscriptionCode'], '144')
        self.assertEqual(response_list[0].query['action'], 'activate')
        self.assertEqual(response_list[0].http_status, 200)

    def test_update_subscriptions(self):
        response_list = update_subscription('javerage', 'activate', [144])

        self.assertEqual(response_list[0].query['subscriptionCode'], '144')
        self.assertEqual(response_list[0].query['action'], 'activate')
        self.assertEqual(response_list[0].http_status, 200)

    def test_modify_subscription_status(self):
        subscriptions = modify_subscription_status(
            'javerage', 233, Subscription.STATUS_ACTIVE)
        self.assertEqual(len(subscriptions), 1)
