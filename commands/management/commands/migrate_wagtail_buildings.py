from decimal import Decimal

from buildings.models import BuildingPage
from django.core.management.base import BaseCommand
from django.db import transaction
from mia_buildings import models as mia_models
from mia_facts.models import City, Country
from mia_people.models import Architect, Developer


class Command(BaseCommand):
    help = "Migrate all wagtail building pages."

    def _add_person(self, building_obj, person_page_queryset, person_is_architect):
        for person_page in person_page_queryset:
            if person_is_architect:
                person = Architect.objects.filter(
                    last_name=person_page.last_name, first_name=person_page.first_name
                ).first()
                if not person:
                    self.stdout.write(
                        self.style.ERROR(
                            f"MiaPerson not found for architect page {person_page.slug}."
                        )
                    )
                    continue
                else:
                    building_obj.architects.add(person)
                    building_obj.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully added architect to {building_obj}"
                        )
                    )
            else:
                person = Developer.objects.filter(
                    last_name=person_page.last_name, first_name=person_page.first_name
                ).first()
                if not person:
                    self.stdout.write(
                        self.style.ERROR(
                            f"MiaPerson not found for developer page {person_page.slug}."
                        )
                    )
                    continue
                else:
                    building_obj.developers.add(person)
                    building_obj.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Successfully added developer to {building_obj}"
                        )
                    )

        return building_obj

    def _add_features(self, building_obj, features, feature_type):
        if feature_type == "building_type":
            mia_feature, created = mia_models.BuildingType.objects.get_or_create(
                name=features.name
            )
            building_obj.building_types.add(mia_feature)
            building_obj.save()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully added {features} to {building_obj}")
            )

            return building_obj

        if feature_type == "access_type":
            mia_feature, created = mia_models.AccessType.objects.get_or_create(
                name=features.name
            )
            building_obj.access_type = mia_feature
            building_obj.save()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully added {features} to {building_obj}")
            )

            return building_obj

        for feature in features:
            if feature_type == "positions":
                mia_feature, created = mia_models.Position.objects.get_or_create(
                    name=feature.name
                )
                building_obj.positions.add(mia_feature)
                building_obj.save()

            if feature_type == "details":
                mia_feature, created = mia_models.Detail.objects.get_or_create(
                    name=feature.name
                )
                building_obj.details.add(mia_feature)
                building_obj.save()

            if feature_type == "windows":
                mia_feature, created = mia_models.Window.objects.get_or_create(
                    name=feature.name
                )
                building_obj.windows.add(mia_feature)
                building_obj.save()

            if feature_type == "roofs":
                mia_feature, created = mia_models.Roof.objects.get_or_create(
                    name=feature.name
                )
                building_obj.roofs.add(mia_feature)
                building_obj.save()

            if feature_type == "facades":
                mia_feature, created = mia_models.Facade.objects.get_or_create(
                    name=feature.name
                )
                building_obj.facades.add(mia_feature)
                building_obj.save()

            if feature_type == "construction_types":
                (
                    mia_feature,
                    created,
                ) = mia_models.ConstructionType.objects.get_or_create(name=feature.name)
                building_obj.construction_types.add(mia_feature)
                building_obj.save()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully added {features} to {building_obj}")
            )

        return building_obj

    def _add_city(self, building_obj, page_city):
        mia_city = City.objects.filter(name=page_city.name).first()
        if not mia_city:
            self.stdout.write(self.style.ERROR(f"City not found: {page_city}"))
            return building_obj

        building_obj.city = mia_city
        building_obj.save()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully added {page_city} to {building_obj}")
        )

        return building_obj

    def _add_country(self, building_obj, page_country):
        mia_country, created = Country.objects.get_or_create(
            country=page_country.country
        )
        building_obj.country = mia_country
        building_obj.save()

        self.stdout.write(
            self.style.SUCCESS(f"Successfully added {page_country} to {building_obj}")
        )

        return building_obj

    def _add_lat_long(self, building_obj, lat_long):
        try:
            page_lat, page_long = (
                lat_long.split(",")[0].strip(),
                lat_long.split(",")[1].strip(),
            )
        except IndexError:
            self.stdout.write(self.style.ERROR(f"Lat/Long not set for {building_obj}"))
            return building_obj

        building_obj.latitude = Decimal(page_lat)
        building_obj.longitude = Decimal(page_long)
        building_obj.save()

        self.stdout.write(
            self.style.SUCCESS(f"Successfully migrated {lat_long} of {building_obj}")
        )

        return building_obj

    def _add_mia_feed_image(self, building_obj, page_feed_image):
        mia_image, created = mia_models.BuildingImage.objects.get_or_create(
            image=page_feed_image.file, building=building_obj
        )
        if created:
            mia_image.is_feed_image = True

            mia_image_tags = mia_image.tags.all()
            if building_obj.country and building_obj.country not in mia_image_tags:
                mia_image.tags.add(building_obj.country.country.name)
            if building_obj.city and building_obj.city not in mia_image_tags:
                mia_image.tags.add(building_obj.city.name)

            mia_image.title = f"{building_obj.name}-feed_image"
            mia_image.save()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully migrated img {mia_image.title}")
            )

        return building_obj

    def _add_mia_images(self, building_obj, page_gallery_images):

        for index, gallery_img in enumerate(page_gallery_images):
            page_image_file = gallery_img.value.get("image")
            if not page_image_file:
                self.stdout.write(
                    self.style.ERROR(f"Image not found in gallery of {building_obj}")
                )
                continue
            page_description = gallery_img.value.get("description")

            mia_image, created = mia_models.BuildingImage.objects.get_or_create(
                image=page_image_file.file, building=building_obj
            )
            if mia_image.is_feed_image:
                continue

            mia_image_tags = mia_image.tags.all()
            if building_obj.country and building_obj.country not in mia_image_tags:
                mia_image.tags.add(building_obj.country.country.name)
            if building_obj.city and building_obj.city not in mia_image_tags:
                mia_image.tags.add(building_obj.city.name)

            mia_image.title = f"{building_obj.name}-{index}"
            mia_image.description = page_description
            mia_image.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully migrated gallery img {mia_image.title}"
                )
            )

        return building_obj

    def handle(self, *args, **options) -> None:
        building_pages = BuildingPage.objects.all()

        for page in building_pages:
            with transaction.atomic():
                mia_building, created = mia_models.Building.objects.get_or_create(
                    name=page.name
                )

                if created:
                    mia_building.todays_use = page.todays_use
                    mia_building.year_of_construction = page.year_of_construction
                    mia_building.directions = page.directions
                    mia_building.description = page.description
                    mia_building.zip_code = page.zip_code
                    mia_building.address = page.address
                    mia_building.protected_monument = page.protected_monument
                    mia_building.storey = page.storey
                    mia_building.is_published = page.live

                    page_architects = page.related_architects.all()
                    mia_building = self._add_person(mia_building, page_architects, True)
                    page_developers = page.related_developers.all()
                    mia_building = self._add_person(
                        mia_building, page_developers, False
                    )

                    page_building_type = page.building_type
                    if page_building_type:
                        mia_building = self._add_features(
                            mia_building, page_building_type, "building_type"
                        )
                    page_access_type = page.access_type
                    if page_access_type:
                        mia_building = self._add_features(
                            mia_building, page_access_type, "access_type"
                        )
                    page_positions = page.positions.all()
                    if page_positions:
                        mia_building = self._add_features(
                            mia_building, page_positions, "positions"
                        )
                    page_details = page.details.all()
                    if page_details:
                        mia_building = self._add_features(
                            mia_building, page_details, "details"
                        )
                    page_windows = page.windows.all()
                    if page_windows:
                        mia_building = self._add_features(
                            mia_building, page_windows, "windows"
                        )
                    page_roofs = page.roofs.all()
                    if page_roofs:
                        mia_building = self._add_features(
                            mia_building, page_roofs, "roofs"
                        )
                    page_facades = page.facades.all()
                    if page_facades:
                        mia_building = self._add_features(
                            mia_building, page_facades, "facades"
                        )
                    page_construction_types = page.construction_types.all()
                    if page_construction_types:
                        mia_building = self._add_features(
                            mia_building, page_construction_types, "construction_types"
                        )

                    if page.city:
                        mia_building = self._add_city(mia_building, page.city)
                    if page.country:
                        mia_building = self._add_country(mia_building, page.country)
                    if page.lat_long:
                        mia_building = self._add_lat_long(mia_building, page.lat_long)
                    if page.feed_image:
                        mia_building = self._add_mia_feed_image(
                            mia_building, page.feed_image
                        )
                    if page.gallery_images:
                        mia_building = self._add_mia_images(
                            mia_building, page.gallery_images
                        )

                self.stdout.write(
                    self.style.SUCCESS(f"Successfully migrated building page {page}")
                )
