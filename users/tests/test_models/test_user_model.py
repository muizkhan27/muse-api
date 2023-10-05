from django.db.utils import DataError, IntegrityError
from django.test import TestCase

from users.models.user import User
from users.tests.factories.user_factory import UserFactory


class BaseTest(TestCase):

    def setUp(self):
        self.user = UserFactory()


class UserModelTests(BaseTest):

    def test_user_object(self):
        self.assertEqual(User.objects.count(), 1)
        UserFactory()
        self.assertEqual(User.objects.count(), 2)

    def test_duplicate_ssn(self):
        with self.assertRaises(IntegrityError):
            UserFactory(ssn=self.user.ssn, first_name='John', last_name='Pork')

    def test_primary_key_available(self):
        with self.assertRaises(IntegrityError):
            UserFactory(ssn=None, first_name='John', last_name='Pork')

    def test_duplicate_email(self):
        with self.assertRaises(IntegrityError):
            UserFactory(ssn=900786010, email=self.user.email)

    def test_email_max_length(self):
        with self.assertRaises(DataError):
            UserFactory(ssn=9876543, email='email'*21)

    def test_first_name_max_length(self):
        with self.assertRaises(DataError):
            UserFactory(ssn=123456, first_name='first'*8)

    def test_last_name_max_length(self):
        with self.assertRaises(DataError):
            UserFactory(ssn=654321, last_name='last'*8)

    def test_full_name(self):
        self.assertEqual(self.user.full_name(), f'{self.user.first_name} {self.user.last_name}')

    def test_str_method(self):
        self.assertEqual(self.user.__str__(), f'{self.user.first_name} {self.user.last_name} ({self.user.email})')
