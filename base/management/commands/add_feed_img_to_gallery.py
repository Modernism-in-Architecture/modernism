from buildings.models import BuildingPage
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Add all feed images to the image gallery of a building."

    def handle(self, *args, **options):

        buildings = BuildingPage.objects.all()

        for building in buildings:

            feed_image = building.feed_image
            new_gallery_image = (
                "image",
                {"image": feed_image, "description": "", "photographer": ""},
            )
            gallery_images = building.gallery_images
            gallery_images.append(new_gallery_image)
            building.gallery_images = gallery_images
            building.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully added feed image to {building.name} gallery."
                )
            )
