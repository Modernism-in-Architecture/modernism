from django.urls import path

from . import views

urlpatterns = [
    path("developers/", views.get_developer_list, name="developer-index-list"),
    path(
        "developers/<slug:slug>/",
        views.get_developer_details,
        name="developer-details",
    ),
    path("architects/", views.get_architect_list, name="architect-index-list"),
    path(
        "architects/<slug:slug>/",
        views.get_architect_details,
        name="architect-details",
    ),
]
