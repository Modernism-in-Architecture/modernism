import time
from django.core.management.base import BaseCommand
from django.db.models.query import Prefetch
from django.utils import timezone

from mia_buildings.models import Building, BuildingImage
from modernism.tools import generate_thumbnails_for_image


class Command(BaseCommand):
    help = "Precreate thumbnails of building images."

    def handle(self, *args, **kwargs):
        self.stdout.write("Get all buildings...")

        start_time = time.time()

        buildings = (
            Building.objects.filter(is_published=True, thumbnails_created=None)
            .prefetch_related(
                Prefetch(
                    "buildingimage_set",
                    queryset=BuildingImage.objects.filter(
                        is_published=True, is_feed_image=True
                    ),
                    to_attr="feed_images",
                )
            )
            .prefetch_related(
                Prefetch(
                    "buildingimage_set",
                    queryset=BuildingImage.objects.filter(
                        is_published=True, is_feed_image=False
                    ),
                    to_attr="gallery_images",
                )
            )
        )

        for building in buildings:
            try:
                self.stdout.write(f"Processing building '{building.name}'...")
                if not building.feed_images:
                    self.stdout.write(
                        f"No feed images for '{building.name}', skipping."
                    )
                    continue
                feed_image = building.feed_images[0].image
                self.stdout.write(f"Generating thumbnails for feed image: {feed_image}")
                generate_thumbnails_for_image(feed_image, is_feed_image=True)

                for gallery_image in building.gallery_images:
                    image = gallery_image.image
                    self.stdout.write(
                        f"Generating thumbnails for gallery image: {image}"
                    )
                    generate_thumbnails_for_image(image, is_feed_image=False)

            except Exception as e:
                self.stdout.write(f"Building '{building.name}': FAILED, , Error: {e}")
                continue

            building.thumbnails_created = timezone.now()
            building.save()

            self.stdout.write(f"{building.name}... DONE")

        end_time = time.time()
        elapsed_time = end_time - start_time
        self.stdout.write(
            f"{buildings.count()} buildings... FINISHED. Took {elapsed_time:.2f} seconds"
        )
