import factory
from factory import LazyAttribute

from users.models.user import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    ssn = factory.Faker('aba')
    email = LazyAttribute(lambda obj: f'{obj.first_name}.{obj.last_name}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
