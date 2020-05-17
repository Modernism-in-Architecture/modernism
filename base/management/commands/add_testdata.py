from datetime import date

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from wagtail.core.models import Page, Site

from architects.models import ArchitectPage, ArchitectsIndexPage
from buildings.models import BuildingPage, BuildingsIndexPage, BuildingType
from home.models import HomePage


@transaction.atomic
def setup_test_data():
    from django.contrib.auth.models import User

    User.objects.create_superuser(
        username="superuser", password="superuser",
    )

    home = HomePage.objects.first()
    home.hero_text = "Modernism in Architecture is awesome!"
    home.save()

    architect_index = ArchitectsIndexPage(
        title="Architect Index",
        intro="Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin. Sesame snaps cookie caramels cheesecake cupcake pastry cake chupa chups danish. Jelly bear claw cake caramels jelly-o brownie. Jelly bear claw sweet roll ice cream dessert tart gingerbread fruitcake. Carrot cake cupcake sugar plum jujubes chocolate cake pudding cake. Pie candy sweet roll liquorice gingerbread bear claw liquorice cake. Bear claw fruitcake soufflé.",
        slug="architect-index",
    )
    home.add_child(instance=architect_index)

    building_index = BuildingsIndexPage(
        title="Building Index",
        intro="Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin. Sesame snaps cookie caramels cheesecake cupcake pastry cake chupa chups danish. Jelly bear claw cake caramels jelly-o brownie. Jelly bear claw sweet roll ice cream dessert tart gingerbread fruitcake. Carrot cake cupcake sugar plum jujubes chocolate cake pudding cake. Pie candy sweet roll liquorice gingerbread bear claw liquorice cake. Bear claw fruitcake soufflé.",
        slug="building-index",
    )
    home.add_child(instance=building_index)

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
        architect=architect_2,
        description="Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin. I tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin.",
        year_of_construction="1924",
        directions="Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant.",
        address="Tůmova 2261/36, (Žabovřesky), Brno, Czech Republic",
        lat_long="49.205307, 16.582682",
    )
    building_2 = BuildingPage(
        title="Another House",
        name="Another House",
        slug="another-house",
        building_type=BuildingType.objects.last(),
        architect=architect_1,
        description="Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin.",
        year_of_construction="1934",
        directions="Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant.",
        address="Demmeringstraße 8, 04177 Leipzig, Germany",
        lat_long="51.338705, 12.336127",
    )
    building_3 = BuildingPage(
        title="A School",
        name="A School",
        slug="a-school",
        building_type=BuildingType.objects.first(),
        architect=architect_1,
        description="Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin. Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin.",
        year_of_construction="1920",
        directions="Cake tiramisu dragée jujubes candy chocolate cake.",
        address="Wachsmuthstraße 20, 04229 Leipzig, Germany",
        lat_long="51.321032, 12.328984",
    )
    building_4 = BuildingPage(
        title="Wonderful new house",
        name="Wonderful new house",
        slug="wonderful-new-house",
        building_type=BuildingType.objects.first(),
        architect=architect_1,
        description="Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin. Cake tiramisu dragée jujubes candy chocolate cake. Bonbon toffee jelly tootsie roll apple pie croissant. Wafer jelly-o pastry fruitcake toffee macaroon muffin.",
        year_of_construction="1920",
        directions="Cake tiramisu dragée jujubes candy chocolate cake.",
        address="Marschnerstraße 25, 04109 Leipzig, Germany",
        lat_long="51.337229, 12.355656",
    )
    building_index.add_child(instance=building_1)
    building_index.add_child(instance=building_2)
    building_index.add_child(instance=building_3)
    building_index.add_child(instance=building_4)


class Command(BaseCommand):
    help = "Add some testdata."

    def handle(self, *args, **options):
        setup_test_data()
        self.stdout.write(self.style.SUCCESS("Successfully inserted testdata."))
