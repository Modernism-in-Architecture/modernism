from buildings import models
from django.core.management.base import BaseCommand
from mia_buildings import models as mia_models


class Command(BaseCommand):
    help = "Migrate all wagtail building features."

    def handle(self, *args, **options) -> None:
        const_types = models.ConstructionType.objects.all()
        facades = models.Facade.objects.all()
        roofs = models.Roof.objects.all()
        windows = models.Window.objects.all()
        details = models.Detail.objects.all()
        positions = models.Position.objects.all()
        build_types = models.BuildingType.objects.all()
        acc_types = models.AccessType.objects.all()

        for type in const_types:
            obj, created = mia_models.ConstructionType.objects.get_or_create(
                name=type.name
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully migrated {type}"))

        for facade in facades:
            obj, created = mia_models.Facade.objects.get_or_create(name=facade.name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully migrated {facade}"))

        for roof in roofs:
            obj, created = mia_models.Roof.objects.get_or_create(name=roof.name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully migrated {roof}"))

        for window in windows:
            obj, created = mia_models.Window.objects.get_or_create(name=window.name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully migrated {window}"))

        for detail in details:
            obj, created = mia_models.Detail.objects.get_or_create(name=detail.name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully migrated {detail}"))

        for position in positions:
            obj, created = mia_models.Position.objects.get_or_create(name=position.name)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully migrated {position}")
                )

        for type in build_types:
            obj, created = mia_models.BuildingType.objects.get_or_create(name=type.name)
            obj.description = type.description
            obj.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully migrated {type}"))

        for type in acc_types:
            obj, created = mia_models.AccessType.objects.get_or_create(name=type.name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully migrated {type}"))
