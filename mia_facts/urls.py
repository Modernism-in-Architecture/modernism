from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_fact_list, name="fact-index-list"),
]
