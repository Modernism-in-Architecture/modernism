from django.db.models.query import Prefetch
from easy_thumbnails.files import get_thumbnailer
from mia_buildings.models import Building, BuildingImage


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
    def get_buildings_data(request):
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
                thumb_url = ""

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
    def get_building_details_data(request, building_id):
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
                feed_image = gallery_image.image
                preview_url = get_thumbnailer(feed_image)["preview"].url
                preview_full_url = request.build_absolute_uri(preview_url)
            except:
                preview_full_url = ""
            gallery_image_urls.append(preview_full_url)

        architects = []
        for architect in building.architects.all():
            architects.append(f"{architect.first_name} {architect.last_name}")

        developers = []
        for developer in building.developers.all():
            developers.append(f"{developer.first_name} {developer.last_name}")

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
            "architects": architects,
            "developers": developers,
        }

        return ResponseDataBuilder.build_success_response(building_data), 200
