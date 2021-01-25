from django.core.management.base import BaseCommand, CommandError
from wagtail.images.models import Image


class Command(BaseCommand):
    help = "Rename images."

    def handle(self, *args, **options):

        images = Image.objects.filter(title__startswith="IMG_20200826")
        for image in images:
            title = image.title
            image.title = title.replace("IMG_20200826", "Löbau")
            image.save()

        images = Image.objects.filter(title__startswith="IMG_20200828")
        for image in images:
            title = image.title
            image.title = title.replace("IMG_20200828", "Dessau")
            image.save()

        self.stdout.write(self.style.SUCCESS("Successfully renamed images."))
