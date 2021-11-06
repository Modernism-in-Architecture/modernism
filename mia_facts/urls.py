from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_fact_list, name="fact-index-list"),
    path("<slug:slug>/", views.get_fact_details, name="fact-details"),
]
