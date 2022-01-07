from django.urls import path

from . import views

urlpatterns = [
    path("building/", views.BuildingView.as_view(), name="buildings"),
]
