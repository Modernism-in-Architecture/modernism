from factory import Faker
from factory.django import DjangoModelFactory
from mia_buildings.models import Building


class BuildingFactory(DjangoModelFactory):
    name = Faker("company")

    class Meta:
        model = Building
