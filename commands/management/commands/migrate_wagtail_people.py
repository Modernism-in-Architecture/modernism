from django.core.management.base import BaseCommand
from django.db import transaction
from mia_facts.models import University
from mia_people.models import Architect, Developer, Professor
from people.models import ArchitectPage, DeveloperPage, ProfessorPage


class Command(BaseCommand):
    help = "Migrate all wagtail people pages to django models."

    def _migrate_person_page_fields(self, django_obj, page):
        django_obj.birthday = page.birthday
        django_obj.birth_year_known_only = page.birth_year_known_only
        django_obj.place_of_birth = (
            page.place_of_birth
        )  # country needs to be separated later
        django_obj.day_of_death = page.day_of_death
        django_obj.death_year_known_only = page.death_year_known_only
        django_obj.place_of_death = (
            page.place_of_death
        )  # country needs to be separated later
        django_obj.description = page.description
        django_obj.is_published = True
        django_obj.save()
        universities = page.universities.all()
        if universities:
            for uni in universities:
                mia_university, created = University.objects.get_or_create(
                    name=uni.name
                )
                if created:
                    mia_university.country = uni.country
                    mia_university.city = uni.city
                    mia_university.description = uni.description
                    mia_university.save()
                django_obj.universities.add(mia_university)
                django_obj.save()

        return django_obj

    def _add_professor_mentors(self, django_professor_obj, professor_page_queryset):
        for professor in professor_page_queryset:
            mentor = Professor.objects.filter(
                last_name=professor.last_name, first_name=professor.first_name
            ).first()
            if mentor:
                django_professor_obj.professor_mentors.add(mentor)
                django_professor_obj.save()

        return django_professor_obj

    def _add_architect_mentors(self, django_architect_obj, architect_page_queryset):
        for architect in architect_page_queryset:
            mentor = Architect.objects.filter(
                last_name=architect.last_name, first_name=architect.first_name
            ).first()
            if mentor:
                django_architect_obj.architect_mentors.add(mentor)
                django_architect_obj.save()

        return django_architect_obj

    def handle(self, *args, **options) -> None:
        developer_pages = DeveloperPage.objects.all()
        architect_pages = ArchitectPage.objects.all()
        professor_pages = ProfessorPage.objects.all()

        with transaction.atomic():
            for page in developer_pages:
                new_dev, created = Developer.objects.get_or_create(
                    last_name=page.last_name, first_name=page.first_name
                )
                if created:
                    new_dev = self._migrate_person_page_fields(new_dev, page)

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully migrated dev page {page.last_name}."
                        )
                    )

            for page in architect_pages:
                new_arch, created = Architect.objects.get_or_create(
                    last_name=page.last_name, first_name=page.first_name
                )

                if created:
                    new_arch = self._migrate_person_page_fields(new_arch, page)

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully migrated arch page {page.last_name}."
                        )
                    )

            for page in architect_pages:
                page_architect_mentors = page.architect_mentors.all()
                page_professor_mentors = page.professor_mentors.all()

                mia_arch = Architect.objects.filter(
                    last_name=page.last_name, first_name=page.first_name
                ).first()

                mia_arch = self._add_architect_mentors(mia_arch, page_architect_mentors)
                mia_arch = self._add_professor_mentors(mia_arch, page_professor_mentors)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully added architect and prof mentors to {mia_arch}."
                    )
                )

            for page in professor_pages:
                new_prof, created = Professor.objects.get_or_create(
                    last_name=page.last_name, first_name=page.first_name
                )

                if created:
                    new_prof = self._migrate_person_page_fields(new_prof, page)
                    new_prof.is_active_architect = page.is_active_architect
                    new_prof.is_active_developer = page.is_active_developer
                    new_prof.save()

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully migrated prof page {page.last_name}."
                        )
                    )

            for page in professor_pages:
                page_architect_mentors = page.architect_mentors.all()
                page_professor_mentors = page.professor_mentors.all()

                mia_prof = Professor.objects.filter(
                    last_name=page.last_name, first_name=page.first_name
                ).first()

                mia_prof = self._add_architect_mentors(mia_prof, page_architect_mentors)
                mia_prof = self._add_professor_mentors(mia_prof, page_professor_mentors)

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully added architect mentors to {mia_prof}."
                    )
                )
