from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^(?P<version>(v1))/buildings/$",
        views.get_buildings_list,
        name="buildings-list",
    ),
    re_path(
        r"^(?P<version>(v1))/buildings/(?P<building_id>[0-9]+)/$",
        views.get_buildings_details,
        name="buildings-detail",
    ),
    re_path(
        r"^(?P<version>(v1))/architects/$",
        views.get_architects_list,
        name="architects-list",
    ),
    re_path(
        r"^(?P<version>(v1))/architects/(?P<architect_id>[0-9]+)/$",
        views.get_architects_details,
        name="architects-detail",
    ),
    re_path(
        r"^(?P<version>(v1))/twitter/get_building_details/$",
        views.get_twitter_building_details,
        name="twitter_building_details",
    ),
    re_path(
        r"^(?P<version>(v1))/twitter/(?P<building_id>[0-9]+)/published_on_twitter/$",
        views.set_building_published_on_twitter,
        name="set_building_published_on_twitter",
    ),
]
