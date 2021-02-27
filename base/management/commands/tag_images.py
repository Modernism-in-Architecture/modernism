from django.core.management.base import BaseCommand, CommandError
from taggit.models import Tag
from wagtail.images.models import Image


class Command(BaseCommand):
    help = "Rename images."

    def handle(self, *args, **options):

        list_of_places = [
            "Leipzig",
            "Löbau",
            "Gera",
            "Weimar",
            "Zwenkau",
            "Berlin",
            "Grimma",
            "Prostějov",
            "Znojmo",
            "Hradec Králové",
            "Liberec",
            "Ostrava",
            "Jablonec",
            "Prague",
            "Brno",
        ]

        for place in list_of_places:
            images = Image.objects.filter(title__startswith=place)
            tag, created = Tag.objects.get_or_create(name=place)
            for image in images:
                image.tags.add(tag)
                image.save()

        self.stdout.write(self.style.SUCCESS("Successfully updated tags of images."))
