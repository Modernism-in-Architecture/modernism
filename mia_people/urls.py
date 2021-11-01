from django.urls import path

from . import views

urlpatterns = [
    path("developers/", views.get_developer_list, name="developer-index-list"),
    path("architects/", views.get_architect_list, name="architect-index-list"),
]
