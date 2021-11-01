from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_building_list, name="building-index-list"),
]
