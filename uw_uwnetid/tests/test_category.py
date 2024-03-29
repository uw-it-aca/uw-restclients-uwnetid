# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from unittest import TestCase
from uw_uwnetid.category import get_netid_categories
from uw_uwnetid.models import Category
from uw_uwnetid.util import fdao_uwnetid_override


@fdao_uwnetid_override
class Office365EduSubsTest(TestCase):

    def test_get_netid_categories(self):
        cats = get_netid_categories('javerage', [])
        self.assertEqual(len(cats), 4)
        self.assertEqual(cats[0].category_code, 4)
        self.assertEqual(cats[3].status_name, "Active")

    def test_get_netid_category_25(self):
        cats = get_netid_categories('javerage', [25])
        self.assertEqual(len(cats), 1)
        self.assertEqual(cats[0].category_code, 25)
        self.assertEqual(cats[0].status_name, "Active")
