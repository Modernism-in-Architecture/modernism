from django.core.serializers import serialize
from django.views.generic.base import TemplateView

from mia_buildings.models import Building
from mia_facts.models import Photographer
from mia_people.models import Architect, Developer


class MainView(TemplateView):
    template_name = "mia_general/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_of_buildings"] = Building.objects.filter(is_published=True).count()
        context["num_of_architects"] = Architect.objects.filter(
            is_published=True
        ).count()
        context["num_of_developers"] = Developer.objects.filter(
            is_published=True
        ).count()
        return context


class AboutView(TemplateView):
    template_name = "mia_general/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        excluded_names = ["Driske", "Dietze"]
        context["photographers"] = Photographer.objects.exclude(last_name__in=excluded_names).order_by("last_name")
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
        buildings = Building.objects.filter(is_published=True)
        context["buildings"] = serialize(
            "json",
            buildings,
            fields=("pk", "latitude", "longitude", "slug", "name", "address"),
        )
        return context


class PrivacyPolicyView(TemplateView):
    template_name = "mia_general/privacy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
