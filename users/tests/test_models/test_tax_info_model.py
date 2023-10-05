from django.db.utils import IntegrityError
from django.test import TestCase

from users.models.user_tax_info import UserTaxInfo
from users.tests.factories.tax_info_factory import UserTaxInfoFactory


class BaseTest(TestCase):

    def setUp(self):
        self.user_tax_info = UserTaxInfoFactory()
        self.user = self.user_tax_info.ssn


class TaxInfoModelTests(BaseTest):

    def test_tax_info_object(self):
        self.assertEqual(UserTaxInfo.objects.count(), 1)
        UserTaxInfoFactory()
        self.assertEqual(UserTaxInfo.objects.count(), 2)

    def test_year_ssn_uniqueness(self):
        with self.assertRaises(IntegrityError):
            UserTaxInfoFactory(ssn=self.user, tax_year=self.user_tax_info.tax_year)

    def test_foreign_key_constraint(self):
        with self.assertRaises(IntegrityError):
            UserTaxInfoFactory(ssn=None, tax_year=2023, tax_info={})
