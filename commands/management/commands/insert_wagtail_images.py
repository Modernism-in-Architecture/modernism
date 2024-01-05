from collections import namedtuple

from django.core.management.base import BaseCommand
from django.db import connection

from mia_buildings.models import BuildingImage


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


class Command(BaseCommand):
    help = "Migrate all wagtail images without a building."

    def handle(self, *args, **options):

        with connection.cursor() as cursor:
            cursor.execute("SELECT title, file FROM wagtailimages_image")
            results = namedtuplefetchall(cursor)
            for result in results:
                images = BuildingImage.objects.filter(image=result[1])
                if not images:
                    BuildingImage.objects.create(title=result[0], image=result[1])
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfully migrated {result[0]}")
                    )
