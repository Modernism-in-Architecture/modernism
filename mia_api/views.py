from django.db.models.query import Prefetch
from mia_buildings.models import Building, BuildingImage
from mia_people.models import Architect
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from mia_api.serializers import (
    ArchhitectDetailSerializerV1,
    ArchhitectListSerializerV1,
    BuildingDetailSerializerV1,
    BuildingListSerializerV1,
)


class BuildingView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

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
                raise NotFound(detail="Building not found", code=404)
            return building

        return self.buildings

    def get_serializer_class(self):
        # version = self.kwargs.get('version', 'v1')
        is_detail_view = bool(self.kwargs.get("building_id"))

        return (
            BuildingDetailSerializerV1 if is_detail_view else BuildingListSerializerV1
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        many = not bool(self.kwargs.get("building_id"))
        serializer = self.get_serializer(
            queryset, many=many, context={"request": request}
        )

        return Response(data=serializer.data, status=200)


class ArchitectView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

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
                raise NotFound(detail="Architect not found", code=404)

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

        return Response(data=serializer.data, status=200)
