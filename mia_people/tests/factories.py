from factory import Faker
from factory.django import DjangoModelFactory
from mia_people.models import Architect, Developer, Professor


class ArchitectFactory(DjangoModelFactory):
    last_name = Faker("last_name")

    class Meta:
        model = Architect


class DeveloperFactory(DjangoModelFactory):
    last_name = Faker("last_name")

    class Meta:
        model = Developer


class ProfessorFactory(DjangoModelFactory):
    last_name = Faker("last_name")

    class Meta:
        model = Professor
