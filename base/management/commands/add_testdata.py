from datetime import date

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from wagtail.core.models import Page, Site

from buildings.models import (
    BuildingPage,
    BuildingPageArchitectRelation,
    BuildingsIndexPage,
    BuildingType,
    City,
    Country,
    PlacesIndexPage,
)
from facts.models import FactsIndexPage
from home.models import HomePage
from people.models import (
    ArchitectPage,
    ArchitectsIndexPage,
    BuildingOwnerPage,
    BuildingOwnersIndexPage,
    DeveloperPage,
    DevelopersIndexPage,
    PersonPage,
    PersonsIndexPage,
)


@transaction.atomic
def setup_test_data():
    from django.contrib.auth.models import User

    User.objects.create_superuser(
        username="superuser", password="superuser",
    )
    root = Page.get_first_root_node()
    site = Site.objects.first()

    old_rootpage = site.root_page
    old_rootpage.slug = "homepage"
    old_rootpage.save()

    home = HomePage(title="Home", slug="home")
    root.add_child(instance=home)

    site.root_page = home
    site.save()

    places_index = PlacesIndexPage(title="Map", slug="maps", show_in_menus=True)
    home.add_child(instance=places_index)

    facts_index = FactsIndexPage(title="Facts", slug="facts", show_in_menus=True,)
    home.add_child(instance=facts_index)

    country = Country.objects.create(country="DE")
    City.objects.create(name="Leipzig", country=country)
    City.objects.create(name="Berlin", country=country)

    building_index = BuildingsIndexPage(
        title="Buildings", slug="buildings", show_in_menus=True,
    )
    home.add_child(instance=building_index)

    person_index = PersonsIndexPage(title="People", slug="people", show_in_menus=True,)
    home.add_child(instance=person_index)

    architect_index = ArchitectsIndexPage(
        title="Architects", slug="architects", show_in_menus=True
    )
    developer_index = DevelopersIndexPage(
        title="Developers", slug="developers", show_in_menus=True
    )
    owner_index = BuildingOwnersIndexPage(
        title="Owners", slug="owners", show_in_menus=True
    )
    person_index.add_child(instance=architect_index)
    person_index.add_child(instance=developer_index)
    person_index.add_child(instance=owner_index)

    architect_1 = ArchitectPage(
        title="Otto Eisler",
        slug="otto-eisler",
        first_name="Otto",
        last_name="Eisler",
        birthday=date(1940, 12, 31),
        day_of_death=date(2002, 4, 4),
        description="Eisler was educated at the Deutsche Technische Hochschule Brünn over the course of ten years, with a likely interruption for military service during World War I. During his studies, he worked at studios in Vienna. Upon graduation, he worked in the architectural practices of Heinrich Tessenow and Walter Gropius before founding his own firm. He also took part in managing his family's business, including his brothers' (Artur, Hugo, Leo, and Moriz) construction company.",
    )
    architect_2 = ArchitectPage(
        title="Jindřich Kumpošt",
        slug="jindrich-kumpost",
        first_name="Jindřich",
        last_name="Kumpošt",
        birthday=date(1940, 12, 31),
        day_of_death=date(2002, 4, 4),
        description="Jindřich Kumpošt was born in Brno on 13 July 1891 in Brno. In 1906 he was admitted to the Czech Polytechnic and then moved to Prostějov, where he worked in the Vulkania arts and crafts company. In 1913 he began to study at the Akademie der bildenden Künste, in Leopold Bauer's studio, in Vienna. He returned to Brno after the war and set up a private design studio; he subsequently became the city's chief architect. He designed the building for the District Sickness Fund, built in Brno in 1922-24. From 1922 onwards he held the office of the chief officer for architecture and urban regulation at the City's Building Authority and was awarded the title of City Building Counsellor in 1924.",
    )
    architect_index.add_child(instance=architect_1)
    architect_index.add_child(instance=architect_2)

    BuildingType.objects.bulk_create(
        [BuildingType(name="School"), BuildingType(name="Apartment Block"),]
    )

    building_1 = BuildingPage(
        title="A House",
        name="A House",
        slug="a-house",
        building_type=BuildingType.objects.last(),
        description="Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin. I tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin.",
        year_of_construction="1924",
        directions="Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant.",
        address="Tůmova 2261/36c",
        lat_long="49.205307, 16.582682",
    )

    building_2 = BuildingPage(
        title="Another House",
        name="Another House",
        slug="another-house",
        building_type=BuildingType.objects.last(),
        description="Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin.",
        year_of_construction="1934",
        directions="Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant.",
        address="Demmeringstraße 8",
        lat_long="51.338705, 12.336127",
    )

    building_3 = BuildingPage(
        title="A School",
        name="A School",
        slug="a-school",
        building_type=BuildingType.objects.first(),
        description="Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin. Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin.",
        year_of_construction="1920",
        directions="Cake tiramisu dragée jujubes candy chocolate cake.",
        address="Wachsmuthstraße 20",
        lat_long="51.321032, 12.328984",
    )

    building_4 = BuildingPage(
        title="Wonderful new house",
        name="Wonderful new house",
        slug="wonderful-new-house",
        building_type=BuildingType.objects.first(),
        description="Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin. Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin.",
        year_of_construction="1920",
        directions="Cake tiramisu dragée jujubes candy chocolate cake.",
        address="Marschnerstraße 25",
        lat_long="51.337229, 12.355656",
    )

    building_index.add_child(instance=building_1)
    building_index.add_child(instance=building_2)
    building_index.add_child(instance=building_3)
    building_index.add_child(instance=building_4)

    BuildingPageArchitectRelation.objects.create(page=building_1, architect=architect_1)
    BuildingPageArchitectRelation.objects.create(page=building_2, architect=architect_1)
    BuildingPageArchitectRelation.objects.create(page=building_3, architect=architect_2)
    BuildingPageArchitectRelation.objects.create(page=building_4, architect=architect_1)


class Command(BaseCommand):
    help = "Add some testdata."

    def handle(self, *args, **options):
        setup_test_data()
        self.stdout.write(self.style.SUCCESS("Successfully inserted testdata."))
