from factory import Sequence, SubFactory
from faker import Faker
from factory.django import DjangoModelFactory
from mia_facts.models import City, Country, Fact


fake = Faker()


class CountryFactory(DjangoModelFactory):
    name = Sequence(lambda n: f"{fake.country()}{n}")

    class Meta:
        model = Country


class CityFactory(DjangoModelFactory):
    name = Sequence(lambda n: f"{fake.city()}{n}")
    country = SubFactory(CountryFactory)

    class Meta:
        model = City


class FactFactory(DjangoModelFactory):
    title = Sequence(lambda n: f"{fake.name()}{n}")

    class Meta:
        model = Fact
