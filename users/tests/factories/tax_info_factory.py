import factory

from users.models.user_tax_info import UserTaxInfo

from .user_factory import UserFactory


class UserTaxInfoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserTaxInfo

    ssn = factory.SubFactory(UserFactory)
    tax_year = factory.Faker('year')
    tax_info = factory.Faker('json')
