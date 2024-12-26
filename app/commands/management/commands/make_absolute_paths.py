from re import sub

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.transaction import atomic
from mia_buildings.models import Building


class Command(BaseCommand):
    help = (
        "Update relative paths in links of history and description HTML to be absolute."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--update",
            action="store_true",
            default=False,
        )

    @atomic
    def handle(self, update, *args, **kwargs):
        if not update:
            self.stdout.write("In dry run mode (--update not passed)")
            return

        self.stdout.write("Get all buildings for updating...")

        buildings = Building.objects.select_for_update()
        for building in buildings:
            building.description = self.substitute_relative_paths(building.description)
            building.history = self.substitute_relative_paths(building.history)

            self.stdout.write(f"{building.name}... DONE")

        if update:
            Building.objects.bulk_update(buildings, ["description", "history"])

            self.stdout.write(f"Finished updating {len(buildings)} Building(s)")

    def substitute_relative_paths(self, text_with_relative_links):
        return sub(
            r"(<a href=['\"])((?:..\/){4,5}(?!..\/))",
            f"\\1{settings.BASE_URL}/",
            text_with_relative_links,
        )
