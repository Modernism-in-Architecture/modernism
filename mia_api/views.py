from django.utils import timezone
from mia_buildings.models import Building
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from mia_api.serializers import (
    BuildingSerializer,
    PersonSerializer,
    SocialMediaSerializer,
)


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
@permission_classes([IsAuthenticated])
def get_buildings_list(request: Request, version: str) -> Response:
    buildings_list_data, status_code = BuildingSerializer.get_buildings_list_data(
        request
    )

    return Response(data=buildings_list_data, status=status_code)


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
@permission_classes([IsAuthenticated])
def get_buildings_details(request: Request, version: str, building_id: int) -> Response:
    buildings_details_data, status_code = BuildingSerializer.get_buildings_details_data(
        request, building_id
    )

    return Response(data=buildings_details_data, status=status_code)


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
@permission_classes([IsAuthenticated])
def get_architects_list(request: Request, version: str) -> Response:
    architects_list_data, status_code = PersonSerializer.get_architects_list_data(
        request
    )

    return Response(data=architects_list_data, status=status_code)


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
@permission_classes([IsAuthenticated])
def get_architects_details(
    request: Request, version: str, architect_id: int
) -> Response:
    architects_details_data, status_code = PersonSerializer.get_architects_details_data(
        request, architect_id
    )

    return Response(data=architects_details_data, status=status_code)


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
@permission_classes([IsAuthenticated])
def get_twitter_building_details(request: Request, version: str) -> Response:
    (
        building_details_data,
        status_code,
    ) = SocialMediaSerializer.get_twitter_building_details(request)

    return Response(data=building_details_data, status=status_code)


@api_view(["PATCH"])
@renderer_classes((JSONRenderer,))
@permission_classes([IsAuthenticated])
def set_building_published_on_twitter(
    request: Request, version: str, building_id: int
) -> Response:
    try:
        building = Building.objects.get(pk=building_id)
    except Building.DoesNotExist:
        return Response(
            data={"error": {"message": "Building does not exist"}}, status=404
        )

    if not building.published_on_twitter:
        building.published_on_twitter = timezone.now()
        building.save()

    return Response(data={}, status=204)
