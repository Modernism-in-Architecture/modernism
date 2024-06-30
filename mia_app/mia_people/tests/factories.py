from factory import Sequence
from faker import Faker
from factory.django import DjangoModelFactory
from mia_people.models import Architect, Developer, Professor


fake = Faker()


class ArchitectFactory(DjangoModelFactory):
    last_name = Sequence(lambda n: f"{fake.last_name()}{n}")

    class Meta:
        model = Architect


class DeveloperFactory(DjangoModelFactory):
    last_name = Sequence(lambda n: f"{fake.last_name()}{n}")

    class Meta:
        model = Developer


class ProfessorFactory(DjangoModelFactory):
    last_name = Sequence(lambda n: f"{fake.last_name()}{n}")

    class Meta:
        model = Professor
