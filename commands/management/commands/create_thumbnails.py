import time

from django.core.management.base import BaseCommand
from django.utils import timezone
from mia_buildings.models import BuildingImage
from modernism.tools import generate_thumbnails_for_image


class Command(BaseCommand):
    help = "Precreate thumbnails of building images."

    def handle(self, *args, **kwargs):
        self.stdout.write("Get all building images...")
        start_time = time.time()

        building_images = BuildingImage.objects.filter(
            is_published=True, thumbnails_created=None
        )
        failed_image_ids = []

        for image in building_images:
            image_name = image.title if image.title else image.pk
            try:
                self.stdout.write(f"Processing image '{image_name}'...")
                generate_thumbnails_for_image(
                    image.image, is_feed_image=image.is_feed_image
                )

            except Exception as e:
                self.stdout.write(f"Building '{image_name}': FAILED, , Error: {e}")
                failed_image_ids.append(image.pk)
                continue

            self.stdout.write(f"{image_name}... DONE")

        building_images.exclude(pk__in=failed_image_ids).update(
            thumbnails_created=timezone.now()
        )

        end_time = time.time()
        elapsed_time = end_time - start_time
        self.stdout.write(
            f"{building_images.count()} buildings... FINISHED. Took {elapsed_time:.2f} seconds"
        )
