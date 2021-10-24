from django.core.management.base import BaseCommand
from facts.models import FactCategory, FactPage
from mia_facts.models import Fact as MiaFact
from mia_facts.models import FactCategory as MiaFactCategory
from mia_facts.models import FactImage as MiaFactImage


class Command(BaseCommand):
    help = "Migrate all wagtail fact pages to django models."

    def handle(self, *args, **options):
        fact_pages = FactPage.objects.all()

        for page in fact_pages:
            new_fact, created = MiaFact.objects.get_or_create(
                title=page.title, description=page.description
            )
            if page.image:
                MiaFactImage.objects.get_or_create(
                    image=page.image.file, fact=new_fact, title=page.image.title
                )

            for wl_fact_cat in page.categories.all():
                new_category, created = MiaFactCategory.objects.get_or_create(
                    name=wl_fact_cat.category
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully migrated category {wl_fact_cat.category}."
                        )
                    )
                new_fact.categories.add(new_category)
                new_fact.save()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully migrated category {new_fact.title}.")
            )
