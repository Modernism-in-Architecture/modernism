from django.shortcuts import render
from django.views.generic.base import TemplateView
from mia_buildings.models import Building


class MainView(TemplateView):

    template_name = "mia_general/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AboutView(TemplateView):

    template_name = "mia_general/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class IntroView(TemplateView):

    template_name = "mia_general/intro.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LegalInfoView(TemplateView):

    template_name = "mia_general/legal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MapView(TemplateView):

    template_name = "mia_general/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PrivacyPolicyView(TemplateView):

    template_name = "mia_general/privacy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
