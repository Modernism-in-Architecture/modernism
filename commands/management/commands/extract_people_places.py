from django.core.management.base import BaseCommand
from django.db import transaction
from mia_facts.models import City, Country
from mia_people.models import Architect, Developer, Professor


class Command(BaseCommand):
    help = "Separate city and country of people"

    def handle(self, *args, **options):
        architects = Architect.objects.all()
        developers = Developer.objects.all()

        for architect in architects:
            with transaction.atomic():
                old_birthplace = architect.place_of_birth
                old_deathplace = architect.place_of_death
                try:
                    birthplace = old_birthplace.split(",")[0].strip()
                    birthcountry = old_birthplace.split(",")[1].strip()
                    deathplace = old_deathplace.split(",")[0].strip()
                    deathcountry = old_deathplace.split(",")[1].strip()
                except IndexError:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Error, handle manually, architect {architect}."
                        )
                    )
                    continue

                birthcountry_obj = Country.objects.filter(
                    name__exact=birthcountry
                ).first()
                if not birthcountry_obj:
                    birthcountry_obj = Country.objects.create(name=birthcountry)

                deathcountry_obj = Country.objects.filter(
                    name__exact=deathcountry
                ).first()
                if not deathcountry_obj:
                    deathcountry_obj = Country.objects.create(name=deathcountry)

                birthplace_obj = City.objects.filter(
                    name__exact=birthplace, country=birthcountry_obj
                ).first()
                if not birthplace_obj:
                    birthplace_obj = City.objects.create(
                        name=birthplace, country=birthcountry_obj
                    )

                deathplace_obj = City.objects.filter(
                    name__exact=deathplace, country=deathcountry_obj
                ).first()
                if not deathplace_obj:
                    deathplace_obj = City.objects.create(
                        name=deathplace, country=deathcountry_obj
                    )

                architect.birth_place = birthplace_obj
                architect.death_place = deathplace_obj

                architect.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully migrated architect {architect}.")
                )

        for developer in developers:
            with transaction.atomic():
                old_birthplace = developer.place_of_birth
                old_deathplace = developer.place_of_death
                try:
                    birthplace = old_birthplace.split(",")[0].strip()
                    birthcountry = old_birthplace.split(",")[1].strip()
                    deathplace = old_deathplace.split(",")[0].strip()
                    deathcountry = old_deathplace.split(",")[1].strip()
                except IndexError:
                    self.stdout.write(
                        self.style.ERROR(f"Error, handle manually, dev {developer}.")
                    )
                    continue

                birthcountry_obj = Country.objects.filter(
                    name__exact=birthcountry
                ).first()
                if not birthcountry_obj:
                    birthcountry_obj = Country.objects.create(name=birthcountry)

                deathcountry_obj = Country.objects.filter(
                    name__exact=deathcountry
                ).first()
                if not deathcountry_obj:
                    deathcountry_obj = Country.objects.create(name=deathcountry)

                birthplace_obj = City.objects.filter(
                    name__exact=birthplace, country=birthcountry_obj
                ).first()
                if not birthplace_obj:
                    birthplace_obj = City.objects.create(
                        name=birthplace, country=birthcountry_obj
                    )

                deathplace_obj = City.objects.filter(
                    name__exact=deathplace, country=deathcountry_obj
                ).first()
                if not deathplace_obj:
                    deathplace_obj = City.objects.create(
                        name=deathplace, country=deathcountry_obj
                    )

                developer.birth_place = birthplace_obj
                developer.death_place = deathplace_obj

                developer.save()
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully migrated architect {developer}.")
                )
