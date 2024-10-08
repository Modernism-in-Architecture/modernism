from django.core.management.base import BaseCommand
from django.db.models.query import Prefetch
from mia_buildings.models import Building, BuildingImage
from modernism.tools import generate_thumbnails_for_image
from django.utils import timezone


class Command(BaseCommand):
    help = "Precreate thumbnails of building images."

    def handle(self, update, *args, **kwargs):
        self.stdout.write("Get all buildings...")

        buildings = (
            Building.objects.filter(is_published=True, thumbnails_created=False)
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
                feed_image = building.feed_images[0].image
                generate_thumbnails_for_image(feed_image, is_feed_image=True)

                for gallery_image in building.gallery_images:
                    image = gallery_image.image
                    generate_thumbnails_for_image(image, is_feed_image=False)

            except Exception as e:
                self.stdout.write(
                    f"{building.name}... Exception during creation, continue..."
                )
                continue

            building.thumbnails_created = timezone.now()
            building.save()

            self.stdout.write(f"{building.name}... DONE")

        self.stdout.write(f"{buildings.count()} buildings... FINISHED")
