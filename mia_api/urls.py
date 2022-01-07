from django.urls import path

from . import views

urlpatterns = [
    path("building/", views.get_buildings, name="buildings"),
]
