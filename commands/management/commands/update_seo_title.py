from distutils.command import build
import logging
from django.core.management.base import BaseCommand
from mia_buildings.models import Building

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Migrate building information into the seo title and truncate if needed."

    def handle(self, *args, **options):

        for building in Building.objects.filter(is_published=True):
            allowed_length_seo_title = 58
            architects = building.architects
            building_name = building.name
            architect_name = ""

            if architects.count() > 2:
                architect_name = f"{architects.first().first_name} {architects.first().last_name} et al."

            if architects.count() == 1:
                architect_name = (
                    f"{architects.first().first_name} {architects.first().last_name}"
                )

            seo_title_end = (
                f" in {building.city.name} by {architect_name}"
                if architect_name
                else f" in {building.city.name}"
            )

            length_of_seo_title_end = len(seo_title_end)
            len_of_building_name = len(building_name)

            if (
                length_of_seo_title_end + len_of_building_name
                > allowed_length_seo_title
            ):
                building_name = f"{building_name[:allowed_length_seo_title-length_of_seo_title_end]}..."
                logger.info(
                    f"Truncated building with pk {building.pk}:\n{building.name}"
                )

            seo_title = f"{building_name}{seo_title_end}"

            building.seo_title = seo_title
            building.save()
