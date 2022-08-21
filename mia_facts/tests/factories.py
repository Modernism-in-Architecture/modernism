import factory
from factory.django import DjangoModelFactory
from mia_facts.models import City, Country


class CountryFactory(DjangoModelFactory):
    name = factory.Faker("country")

    class Meta:
        model = Country


class CityFactory(DjangoModelFactory):
    name = factory.Faker("city")
    country = factory.SubFactory(CountryFactory)

    class Meta:
        model = City
