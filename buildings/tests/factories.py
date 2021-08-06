import factory
from buildings.models import (
    AccessType,
    BuildingPage,
    BuildingPageArchitectRelation,
    BuildingPageDeveloperRelation,
    BuildingsIndexPage,
    BuildingType,
    City,
    ConstructionType,
    Country,
    Detail,
    Facade,
    Position,
    Roof,
    Window,
)
from django_countries import countries
from factory import fuzzy
from home.models import HomePage
from people.models import (
    ArchitectPage,
    ArchitectsIndexPage,
    DeveloperPage,
    DevelopersIndexPage,
    PersonsIndexPage,
)
from wagtail.core.models import Page


class BuildingTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BuildingType

    name = factory.Sequence(lambda n: f"Building type {n}")


class AccessTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AccessType

    name = factory.Sequence(lambda n: f"Access type {n}")


class ConstructionTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ConstructionType

    name = factory.Sequence(lambda n: f"Construction type {n}")


class FacadeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Facade

    name = factory.Sequence(lambda n: f"Facade type {n}")


class RoofFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Roof

    name = factory.Sequence(lambda n: f"Roof type {n}")


class WindowFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Window

    name = factory.Sequence(lambda n: f"Window type {n}")


class DetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Detail

    name = factory.Sequence(lambda n: f"Detail type {n}")


class PositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Position

    name = factory.Sequence(lambda n: f"Position type {n}")


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    country = factory.fuzzy.FuzzyChoice(list(countries), getter=lambda c: c[0])


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = factory.Sequence(lambda n: f"Position type {n}")


class PageFactory(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        try:
            parent = kwargs.pop("parent")
        except KeyError:
            parent = Page.get_first_root_node()

        page = model_class(*args, **kwargs)
        parent.add_child(instance=page)

        return page


class HomePageFactory(PageFactory):
    class Meta:
        model = HomePage

    title = factory.Sequence(lambda n: f"Home page {n}")


class BuildingsIndexPageFactory(PageFactory):
    class Meta:
        model = BuildingsIndexPage

    title = factory.Sequence(lambda n: f"Building index page {n}")


class PersonsIndexPageFactory(PageFactory):
    class Meta:
        model = PersonsIndexPage

    title = factory.Sequence(lambda n: f"Person index page {n}")


class ArchitectsIndexPageFactory(PageFactory):
    class Meta:
        model = ArchitectsIndexPage

    title = factory.Sequence(lambda n: f"Architect index page {n}")


class DevelopersIndexPageFactory(PageFactory):
    class Meta:
        model = DevelopersIndexPage

    title = factory.Sequence(lambda n: f"Developer index page {n}")


class ArchitectPageFactory(PageFactory):
    class Meta:
        model = ArchitectPage

    title = factory.Sequence(lambda n: f"Architect page {n}")
    last_name = factory.Sequence(lambda n: f"Architect {n}")


class DeveloperPageFactory(PageFactory):
    class Meta:
        model = DeveloperPage

    title = factory.Sequence(lambda n: f"Building page {n}")
    last_name = factory.Sequence(lambda n: f"Developer {n}")


class BuildingPageArchitectRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BuildingPageArchitectRelation


class BuildingPageDeveloperRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BuildingPageDeveloperRelation


class BuildingPageFactory(PageFactory):
    class Meta:
        model = BuildingPage

    title = factory.Sequence(lambda n: f"Building page {n}")
    name = factory.Sequence(lambda n: f"Building {n}")
    lat_long = "64.144367,-21.939182"

    @factory.post_generation
    def generate_features(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for construction_type in extracted:
                self.construction_types.add(construction_type)
