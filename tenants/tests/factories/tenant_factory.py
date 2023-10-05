import factory
from factory import LazyAttribute

from tenants.models import Tenant


class TenantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tenant

    name = factory.Faker('first_name')
    email = LazyAttribute(lambda obj: f'{obj.name}@example.com')
    password = factory.Faker('password')
    address = factory.Faker('address')
    date_joined = factory.Faker('date_time')
    subdomain = LazyAttribute(lambda obj: f'{obj.name}')
