from django.db.models.query import Prefetch
from easy_thumbnails.files import get_thumbnailer
from mia_buildings.models import Building, BuildingImage
from mia_facts.models import Source
from mia_people.models import Architect


class ResponseDataBuilder:
    @staticmethod
    def build_error_response(error_message, error_fields=None):
        error_data = {"message": error_message}
        if error_fields is not None:
            error_data.update({"fields": error_fields})

        response = {"error": error_data}

        return response

    @staticmethod
    def build_success_response(data):
        return {"data": data}


class BuildingSerializer:
    @staticmethod
    def get_buildings_list_data(request):
        buildings_data = []

        buildings = (
            Building.objects.filter(is_published=True)
            .select_related("city__country")
            .prefetch_related(
                Prefetch(
                    "buildingimage_set",
                    queryset=BuildingImage.objects.filter(
                        is_published=True, is_feed_image=True
                    ),
                    to_attr="feed_images",
                )
            )
            .order_by("-created")
        )

        for building in buildings:

            try:
                feed_image = building.feed_images[0].image
                thumb_url = get_thumbnailer(feed_image)["feed"].url
                thumb_full_url = request.build_absolute_uri(thumb_url)
            except:
                thumb_full_url = ""

            building_data = {
                "id": building.pk,
                "name": building.name,
                "yearOfConstruction": building.year_of_construction,
                "city": building.city.name,
                "country": building.city.country.name,
                "latitude": building.latitude,
                "longitude": building.longitude,
                "feedImage": thumb_full_url,
            }
            buildings_data.append(building_data)

        return ResponseDataBuilder.build_success_response(buildings_data), 200

    @staticmethod
    def get_buildings_details_data(request, building_id):
        building_data = {}

        building = (
            Building.objects.filter(pk=building_id, is_published=True)
            .select_related("city__country")
            .prefetch_related("architects")
            .prefetch_related("developers")
            .prefetch_related(
                Prefetch(
                    "buildingimage_set",
                    queryset=BuildingImage.objects.filter(is_published=True),
                    to_attr="gallery_images",
                )
            )
            .first()
        )

        if not building:
            return ResponseDataBuilder.build_error_response("Building not found"), 404

        gallery_image_urls = []
        for gallery_image in building.gallery_images:
            try:
                image = gallery_image.image
                mobile_img_url = get_thumbnailer(image)["mobile"].url
                mobile_img_full_url = request.build_absolute_uri(mobile_img_url)
            except:
                mobile_img_full_url = ""
            gallery_image_urls.append(mobile_img_full_url)

        architects = []
        for architect in building.architects.all():
            architects.append(f"{architect.first_name} {architect.last_name}")

        developers = []
        for developer in building.developers.all():
            developers.append(f"{developer.first_name} {developer.last_name}")

        web_sources = []
        for source in building.sources.filter(source_type=Source.SourceType.WEBSITE):
            web_sources.append(
                {"id": source.id, "title": source.title, "url": source.url}
            )

        book_sources = []
        for source in building.sources.filter(
            source_type__in=[Source.SourceType.BOOK, Source.SourceType.JOURNAL]
        ).prefetch_related("authors"):
            book_sources.append(
                {
                    "id": source.id,
                    "authorsLastNames": source.authors.values_list(
                        "last_name", flat=True
                    ),
                    "title": source.title,
                    "year": source.year,
                }
            )

        building_data = {
            "id": building.pk,
            "name": building.name,
            "yearOfConstruction": building.year_of_construction,
            "isProtected": building.protected_monument,
            "address": building.address,
            "zipCode": building.zip_code,
            "city": building.city.name,
            "country": building.city.country.name,
            "latitude": building.latitude,
            "longitude": building.longitude,
            "galleryImages": gallery_image_urls,
            "subtitle": building.subtitle,
            "todays_use": building.todays_use,
            "history": building.history,
            "description": building.description,
            "directions": building.directions,
            "sourceUrls": web_sources,
            "sourceBooks": book_sources,
            "architects": architects,
            "developers": developers,
        }

        return ResponseDataBuilder.build_success_response(building_data), 200


class PersonSerializer:
    @staticmethod
    def get_architects_list_data(request):
        architects = Architect.objects.filter(is_published=True).order_by("last_name")
        architects_data = [
            {
                "id": architect.pk,
                "lastName": architect.last_name,
                "firstName": architect.first_name,
            }
            for architect in architects
        ]

        return ResponseDataBuilder.build_success_response(architects_data), 200

    @staticmethod
    def get_architects_details_data(request, architect_id):
        architect_data = {}

        architect = (
            Architect.objects.filter(pk=architect_id)
            .select_related("birth_place__country")
            .select_related("death_place__country")
            .first()
        )

        if not architect:
            return ResponseDataBuilder.build_error_response("Architect not found"), 404

        related_buildings = Building.objects.filter(
            is_published=True, architects__id=architect.id
        ).prefetch_related(
            Prefetch(
                "buildingimage_set",
                queryset=BuildingImage.objects.filter(is_feed_image=True),
                to_attr="feed_images",
            )
        )

        related_buildings_data = []
        for related_building in related_buildings:
            try:
                feed_image = related_building.feed_images[0].image
                thumb_url = get_thumbnailer(feed_image)["feed"].url
                thumb_full_url = request.build_absolute_uri(thumb_url)
            except:
                thumb_full_url = ""

            building_data = {
                "id": related_building.pk,
                "name": related_building.name,
                "yearOfConstruction": related_building.year_of_construction,
                "city": related_building.city.name,
                "country": related_building.city.country.name,
                "latitude": related_building.latitude,
                "longitude": related_building.longitude,
                "feedImage": thumb_full_url,
            }
            related_buildings_data.append(building_data)

        web_sources = []
        for source in architect.sources.filter(source_type=Source.SourceType.WEBSITE):
            web_sources.append(
                {"id": source.id, "title": source.title, "url": source.url}
            )

        book_sources = []
        for source in architect.sources.filter(
            source_type__in=[Source.SourceType.BOOK, Source.SourceType.JOURNAL]
        ).prefetch_related("authors"):
            book_sources.append(
                {
                    "id": source.id,
                    "authorsLastNames": source.authors.values_list(
                        "last_name", flat=True
                    ),
                    "title": source.title,
                    "year": source.year,
                }
            )

        architect_data = {
            "id": architect.pk,
            "lastName": architect.last_name,
            "firstName": architect.first_name,
            "birthDay": architect.birthday,
            "birthPlace": architect.birth_place.name if architect.birth_place else "",
            "birthCountry": architect.birth_place.country.name
            if architect.birth_place and architect.birth_place.country
            else "",
            "deathDay": architect.day_of_death,
            "deathPlace": architect.death_place.name if architect.death_place else "",
            "deathCountry": architect.death_place.country.name
            if architect.death_place and architect.death_place.country
            else "",
            "description": architect.description,
            "source_urls": web_sources,
            "source_books": book_sources,
            "relatedBuildings": related_buildings_data,
        }

        return ResponseDataBuilder.build_success_response(architect_data), 200
