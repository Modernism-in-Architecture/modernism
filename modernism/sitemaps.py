from django.contrib import sitemaps
from django.urls import reverse
from mia_buildings.models import Building
from mia_facts.models import Fact
from mia_people.models import Architect, Developer, Professor


class StaticViewSitemap(sitemaps.Sitemap):
    def items(self):
        return ["main", "about", "intro"]

    def location(self, item):
        return reverse(item)


class BuildingsSitemap(sitemaps.Sitemap):
    def items(self):
        return Building.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return reverse("building-details", kwargs={"slug": obj.slug})


class ArchitectsSitemap(sitemaps.Sitemap):
    def items(self):
        return Architect.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return reverse("architect-details", kwargs={"slug": obj.slug})


class DevelopersSitemap(sitemaps.Sitemap):
    def items(self):
        return Developer.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return reverse("developer-details", kwargs={"slug": obj.slug})


class ProfessorsSitemap(sitemaps.Sitemap):
    def items(self):
        return Professor.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return reverse("professor-details", kwargs={"slug": obj.slug})


class FactsSitemap(sitemaps.Sitemap):
    def items(self):
        return Fact.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return reverse("fact-details", kwargs={"slug": obj.slug})
