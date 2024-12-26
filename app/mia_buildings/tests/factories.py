from factory import Sequence
from factory.django import DjangoModelFactory
from faker import Faker

from mia_buildings.models import Building

fake = Faker()


class BuildingFactory(DjangoModelFactory):
    name = Sequence(lambda n: f"{fake.catch_phrase()} {n}")

    class Meta:
        model = Building
