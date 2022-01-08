from django.urls import path

from . import views

urlpatterns = [
    path("building/", views.get_buildings, name="buildings"),
    path(
        "building/<int:building_id>/",
        views.get_building_details,
        name="building_details",
    ),
]
