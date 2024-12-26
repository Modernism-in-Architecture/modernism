import logging

import pyhtml2md
from django.conf import settings
from easy_thumbnails.files import get_thumbnailer
from mia_buildings.models import Building
from mia_people.models import Architect
from modernism.tools import create_thumbnail_image_path
from rest_framework.serializers import (
    BooleanField,
    CharField,
    FloatField,
    ModelSerializer,
    SerializerMethodField,
)

logger = logging.getLogger(__name__)

options = pyhtml2md.Options()
options.splitLines = False


class ArchitectBaseSerializer(ModelSerializer):
    class Meta:
        model = Architect
        fields = ["id", "last_name", "first_name"]


class BuildingBaseSerializer(ModelSerializer):
    city = CharField(source="city.name")
    country = CharField(source="city.country.name")
    latitude = FloatField()
    longitude = FloatField()
    architects = ArchitectBaseSerializer(many=True)
    feed_image = SerializerMethodField()

    class Meta:
        model = Building
        fields = [
            "id",
            "name",
            "year_of_construction",
            "city",
            "country",
            "latitude",
            "longitude",
            "architects",
            "feed_image",
        ]

    def get_feed_image(self, obj):
        request = self.context.get("request")
        feed_image = obj.feed_images[0] if obj.feed_images else None
        feed_thumb_full_url = ""

        if feed_image:
            if not feed_image.thumbnails_created:
                try:
                    feed_thumb_url = get_thumbnailer(feed_image.image)["feed"].url
                    feed_thumb_full_url = request.build_absolute_uri(feed_thumb_url)

                except Exception as err:
                    logger.info(
                        f"Error generating thumbnails for building {obj.id}: {str(err)}"
                    )

            else:
                feed_thumb_full_url = create_thumbnail_image_path(
                    feed_image.image.name, settings.THUMBNAIL_PATHS.get("feed")
                )

        return feed_thumb_full_url


class BuildingDetailSerializerV1(BuildingBaseSerializer):
    gallery_images = SerializerMethodField()
    building_type = SerializerMethodField()
    history_markdown = SerializerMethodField()
    description_markdown = SerializerMethodField()
    absoluteURL = SerializerMethodField()  # noqa: N815
    is_protected = BooleanField(source="protected_monument")

    class Meta(BuildingBaseSerializer.Meta):
        fields = BuildingBaseSerializer.Meta.fields + [
            "gallery_images",
            "is_protected",
            "address",
            "zip_code",
            "subtitle",
            "todays_use",
            "building_type",
            "history",
            "history_markdown",
            "description",
            "description_markdown",
            "directions",
            "absoluteURL",
        ]

    def get_gallery_images(self, obj):
        request = self.context.get("request")
        gallery_image_urls = []
        for gallery_image in obj.gallery_images:
            mobile_img_full_url = ""

            if not gallery_image.thumbnails_created:
                try:
                    image = gallery_image.image
                    mobile_img_url = get_thumbnailer(image)["mobile"].url
                    mobile_img_full_url = request.build_absolute_uri(mobile_img_url)
                except Exception as err:
                    logger.info(
                        f"Error generating gallery thumbnails for building {obj.id}: {str(err)}"
                    )
            else:
                mobile_img_full_url = create_thumbnail_image_path(
                    gallery_image.image.name, settings.THUMBNAIL_PATHS.get("mobile")
                )

            if mobile_img_full_url:
                gallery_image_urls.append(mobile_img_full_url)

        return gallery_image_urls

    def get_building_type(self, obj):
        return obj.building_types.first().name if obj.building_types.exists() else ""

    def get_description_markdown(self, obj):
        converter = pyhtml2md.Converter(obj.description, options)
        return converter.convert()

    def get_history_markdown(self, obj):
        converter = pyhtml2md.Converter(obj.history, options)
        return converter.convert()

    def get_absoluteURL(self, obj):  # noqa: N802
        request = self.context.get("request")
        return f"https://{request.get_host()}/buildings/{obj.slug}/"


class BuildingListSerializerV1(BuildingBaseSerializer):
    preview_image = SerializerMethodField()
    building_type = SerializerMethodField()

    class Meta(BuildingBaseSerializer.Meta):
        fields = BuildingBaseSerializer.Meta.fields + ["preview_image", "building_type"]

    def get_preview_image(self, obj):
        request = self.context.get("request")
        feed_image = obj.feed_images[0]
        preview_thumb_full_url = ""

        if not feed_image.thumbnails_created:
            try:
                preview_thumb_url = get_thumbnailer(feed_image.image)["preview"].url
                preview_thumb_full_url = request.build_absolute_uri(preview_thumb_url)

            except Exception as err:
                logger.info(
                    f"Error generating thumbnails for building {obj.id}: {str(err)}"
                )

        else:
            preview_thumb_full_url = create_thumbnail_image_path(
                feed_image.image.name, settings.THUMBNAIL_PATHS.get("preview")
            )

        return preview_thumb_full_url

    def get_building_type(self, obj):
        return "no type"


class ArchhitectDetailSerializerV1(ArchitectBaseSerializer):
    birth_country = SerializerMethodField()
    birth_place = SerializerMethodField()
    birth_day = SerializerMethodField()
    death_day = SerializerMethodField()
    death_place = SerializerMethodField()
    death_country = SerializerMethodField()
    description_markdown = SerializerMethodField()
    absoluteURL = SerializerMethodField()  # noqa: N815
    related_buildings = SerializerMethodField()

    class Meta(ArchitectBaseSerializer.Meta):
        fields = ArchitectBaseSerializer.Meta.fields + [
            "birth_day",
            "birth_place",
            "birth_country",
            "death_day",
            "death_place",
            "death_country",
            "description",
            "description_markdown",
            "related_buildings",
            "absoluteURL",
        ]

    def get_birth_day(self, obj):
        return obj.birthday if obj.birthday else ""

    def get_birth_place(self, obj):
        return obj.birth_place.name if obj.birth_place else ""

    def get_birth_country(self, obj):
        return (
            obj.birth_place.country.name
            if obj.birth_place and obj.birth_place.country
            else ""
        )

    def get_death_day(self, obj):
        return obj.day_of_death if obj.day_of_death else ""

    def get_death_place(self, obj):
        return obj.death_place.name if obj.death_place else ""

    def get_death_country(self, obj):
        return (
            obj.death_place.country.name
            if obj.death_place and obj.death_place.country
            else ""
        )

    def get_description_markdown(self, obj):
        converter = pyhtml2md.Converter(obj.description, options)
        return converter.convert()

    def get_related_buildings(self, obj):
        buildings = self.context.get("related_buildings")
        serializer = BuildingBaseSerializer(buildings, many=True)
        return serializer.data

    def get_absoluteURL(self, obj):  # noqa: N802
        request = self.context.get("request")
        return f"https://{request.get_host()}/people/architects/{obj.slug}/"


class ArchhitectListSerializerV1(ArchitectBaseSerializer):
    class Meta(ArchitectBaseSerializer.Meta):
        fields = ArchitectBaseSerializer.Meta.fields
