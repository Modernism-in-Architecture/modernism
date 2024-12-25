from django.urls import path

from mia_api.views import ArchitectView, BuildingsCountView, BuildingView

urlpatterns = [
    path("<str:version>/buildings/", BuildingView.as_view(), name="buildings-list"),
    path(
        "<str:version>/buildings/<int:building_id>/",
        BuildingView.as_view(),
        name="buildings-detail",
    ),
    path(
        "<str:version>/buildings/count/",
        BuildingsCountView.as_view(),
        name="buildings-count",
    ),
    path("<str:version>/architects/", ArchitectView.as_view(), name="architects-list"),
    path(
        "<str:version>/architects/<int:architect_id>/",
        ArchitectView.as_view(),
        name="architects-detail",
    ),
]
