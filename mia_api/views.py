from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from mia_api.serializers import (
    BuildingSerializer,
    PersonSerializer,
    SocialMediaSerializer,
)


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
@permission_classes([IsAuthenticated])
def get_buildings_list(request, version):

    buildings_list_data, status_code = BuildingSerializer.get_buildings_list_data(
        request
    )

    return Response(data=buildings_list_data, status=status_code)


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
@permission_classes([IsAuthenticated])
def get_buildings_details(request, version, building_id):

    buildings_details_data, status_code = BuildingSerializer.get_buildings_details_data(
        request, building_id
    )

    return Response(data=buildings_details_data, status=status_code)


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
@permission_classes([IsAuthenticated])
def get_architects_list(request, version):

    architects_list_data, status_code = PersonSerializer.get_architects_list_data(
        request
    )

    return Response(data=architects_list_data, status=status_code)


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
@permission_classes([IsAuthenticated])
def get_architects_details(request, version, architect_id):

    architects_details_data, status_code = PersonSerializer.get_architects_details_data(
        request, architect_id
    )

    return Response(data=architects_details_data, status=status_code)


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
# @permission_classes([IsAuthenticated])
def get_twitter_building_details(request, version):

    (
        building_details_data,
        status_code,
    ) = SocialMediaSerializer.get_twitter_building_details(request)

    return Response(data=building_details_data, status=status_code)
