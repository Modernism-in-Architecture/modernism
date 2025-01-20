import logging

from django.db.models.query import Prefetch
from mia_buildings.models import Building, BuildingImage
from mia_people.models import Architect
from modernism.tools import normalize_to_utc, parse_date_with_timezone
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from mia_api.permissions import IsAuthenticatedOrAdminUser
from mia_api.serializers import (
    ArchhitectDetailSerializerV1,
    ArchhitectListSerializerV1,
    BuildingDetailSerializerV1,
    BuildingListSerializerV1,
)

logger = logging.getLogger(__name__)


class BuildingView(GenericAPIView):
    permission_classes = [IsAuthenticatedOrAdminUser]

    buildings = (
        Building.objects.filter(is_published=True)
        .select_related("city__country")
        .prefetch_related("building_types")
        .prefetch_related(
            Prefetch(
                "architects",
                queryset=Architect.objects.filter(is_published=True),
                to_attr="published_architects",
            )
        )
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

    def get_queryset(self):
        building_id = self.kwargs.get("building_id")

        if building_id:
            logger.debug(f"Building found for id: {building_id}.")
            building = (
                self.buildings.filter(id=building_id)
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
                raise NotFound(
                    detail="Building not found", code=status.HTTP_404_NOT_FOUND
                )
            return building

        logger.debug(f"Return {self.buildings.count()} buildings")
        return self.buildings

    def get_serializer_class(self):
        # version = self.kwargs.get('version', 'v1')
        is_detail_view = bool(self.kwargs.get("building_id"))
        logger.debug(f"Detail view requested: {is_detail_view}")

        return (
            BuildingDetailSerializerV1 if is_detail_view else BuildingListSerializerV1
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        many = not bool(self.kwargs.get("building_id"))

        logger.debug(f"Is Building List call: {many}")

        serializer = self.get_serializer(
            queryset, many=many, context={"request": request}
        )

        response_data = {"data": serializer.data}

        return Response(data=response_data, status=status.HTTP_200_OK)


class BuildingsCountView(GenericAPIView):
    permission_classes = [IsAuthenticatedOrAdminUser]
    queryset = Building.objects.filter(is_published=True)

    def get(self, request, *args, **kwargs):
        date_param = request.query_params.get("since", None)

        try:
            if date_param:
                parsed_date = parse_date_with_timezone(date_param)
                normalized_parsed_date = normalize_to_utc(parsed_date)

                buildings = self.get_queryset().filter(
                    created__gte=normalized_parsed_date
                )
            else:
                buildings = self.get_queryset()

            count = buildings.count()

            return Response(data={"count": count}, status=status.HTTP_200_OK)

        except ValueError:
            return Response(
                {"error": "Invalid date format. Use 2024-12-25T22:34:26.365+01:00"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ArchitectView(GenericAPIView):
    permission_classes = [IsAuthenticatedOrAdminUser]
    architects = Architect.objects.filter(is_published=True).order_by("last_name")

    def get_queryset(self):
        architect_id = self.kwargs.get("architect_id")

        if architect_id:
            architect = (
                self.architects.filter(id=architect_id)
                .select_related("birth_place__country")
                .select_related("death_place__country")
                .first()
            )
            if not architect:
                raise NotFound(
                    detail="Architect not found", code=status.HTTP_404_NOT_FOUND
                )

            return architect

        return self.architects

    def get_serializer_class(self):
        # version = self.kwargs.get('version', 'v1')
        is_detail_view = bool(self.kwargs.get("architect_id"))

        return (
            ArchhitectDetailSerializerV1
            if is_detail_view
            else ArchhitectListSerializerV1
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        architect_id = self.kwargs.get("architect_id")
        many = True
        related_buildings = []

        if architect_id:
            many = False
            related_buildings = (
                Building.objects.filter(is_published=True, architects__id=architect_id)
                .select_related("city__country")
                .prefetch_related(
                    Prefetch(
                        "buildingimage_set",
                        queryset=BuildingImage.objects.filter(is_feed_image=True),
                        to_attr="feed_images",
                    )
                )
            )

        serializer = self.get_serializer(
            queryset,
            many=many,
            context={"request": request, "related_buildings": related_buildings},
        )

        response_data = {"data": serializer.data}

        return Response(data=response_data, status=status.HTTP_200_OK)
