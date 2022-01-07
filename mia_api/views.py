from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


@api_view(["GET"])
@renderer_classes((JSONRenderer,))
@permission_classes([IsAuthenticated])
def get_buildings(request):

    content = {"message": "Hello, World!"}
    status_code = 200

    return Response(data=content, status=status_code)
