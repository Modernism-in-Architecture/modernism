from django.urls import path

from . import views

urlpatterns = [
    path("", views.MainView.as_view(), name="main"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("intro/", views.IntroView.as_view(), name="intro"),
    path("legal-info/", views.LegalInfoView.as_view(), name="legal"),
    path("map/", views.MapView.as_view(), name="map"),
    path("privacy-policy/", views.PrivacyPolicyView.as_view(), name="privacy"),
]
