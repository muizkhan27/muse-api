
import environ
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from tenants.tests.factories.tenant_factory import TenantFactory
from tenants.utils.token_utility import generate_refresh_token

env = environ.Env(
  DEBUG=(bool, False)
)
environ.Env.read_env()


class BaseTest(TestCase):

    def setUp(self):
        self.token_url = reverse('token-view')
        self.refresh_token_url = reverse('refresh-token-view')
        self.client = Client(SERVER_NAME=env('HOST'))
        self.tenant = TenantFactory(email='user@example.com', password='12345678')
        self.refresh_token = generate_refresh_token(self.tenant.id)
        self.expired_refresh_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZW5hbnRfaWQiOjEsImV4cCI6MTY4MDExNDYzNC\
wiaWF0IjoxNjgwMTE0NjM0fQ.pMLuhMHwJmNoMaEtXPju2ZRXVb1ID0S5Dz450aH6FTU'


class AuthenticationTests(BaseTest):

    # Helpers

    def status_is_200(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def status_is_201(self, response):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def status_is_400(self, response):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Tests

    def test_token_view(self):
        data = {'email': 'user@example.com', 'password': '12345678'}
        response = self.client.post(self.token_url, data=data)
        self.status_is_201(response)

    def test_token_view_with_invalid_data(self):
        data = {'email': 'user@example.com', 'password': '12345'}
        response = self.client.post(self.token_url, data=data)
        self.assertEqual(response.content, b'{"Error":"Email or password is incorrect."}')
        self.status_is_400(response)

    def test_refresh_token(self):
        response = self.client.post(self.refresh_token_url, data={'refresh_token': self.refresh_token})
        self.status_is_200(response)

    def test_invalid_refresh_token(self):
        token = 'nbchdhcjwid3284832rbfejhbdcfewf233wefvfbsfdgsdvgsdfvDSVsd'
        response = self.client.post(self.refresh_token_url, data={'refresh_token': token})
        self.assertEqual(response.content, b'"Not enough segments"')
        self.status_is_400(response)

    def test_expired_refresh_token(self):
        response = self.client.post(self.refresh_token_url, data={'refresh_token': self.expired_refresh_token})
        self.assertEqual(response.content, b'"Signature has expired"')
        self.status_is_400(response)
