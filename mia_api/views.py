from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from mia_api.serializers import BuildingSerializer


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
@permission_classes([IsAuthenticated])
def get_buildings(request):

    buildings_data, status_code = BuildingSerializer.get_buildings_data(request)

    return Response(data=buildings_data, status=status_code)
