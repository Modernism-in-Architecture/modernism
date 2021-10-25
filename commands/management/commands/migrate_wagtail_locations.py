from django.core.management.base import BaseCommand
from facts.models import City, Country
from mia_facts.models import City as MiaCity
from mia_facts.models import Country as MiaCountry


class Command(BaseCommand):
    help = "Migrate all wagtail locations to django models."

    def handle(self, *args, **options) -> None:
        countries = Country.objects.all()
        cities = City.objects.all()

        for country in countries:
            mia_country, created = MiaCountry.objects.get_or_create(
                country=country.country
            )
            mia_country.description = country.description
            mia_country.save()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully migrated {country.country.name}")
            )

        for city in cities:
            mia_city, created = MiaCity.objects.get_or_create(name=city.name)
            mia_city.description = city.description
            if city.country:
                mia_country = MiaCountry.objects.filter(
                    country=city.country.country
                ).first()
                mia_city.country = mia_country
            mia_city.save()
            self.stdout.write(self.style.SUCCESS(f"Successfully migrated {city.name}"))
