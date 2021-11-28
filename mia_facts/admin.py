from django.contrib import admin
from django.db import models
from django.forms.widgets import TextInput
from tinymce.widgets import TinyMCE

from .models import (
    Author,
    City,
    Country,
    Fact,
    FactCategory,
    FactImage,
    Photographer,
    Source,
    University,
)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "city",
    ]
    search_fields = ["name", "city__name", "city__country__name"]
    ordering = ["name"]
    autocomplete_fields = ["city"]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ["name", "country"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    filter_horizontal = ["authors"]


class FactImageInline(admin.StackedInline):
    model = FactImage
    extra = 0
    classes = ["collapse"]


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    search_fields = ["title", "description"]
    list_display = ["title", "pk", "is_published", "get_categories", "created"]
    list_filter = ["categories"]
    filter_horizontal = ["categories", "sources"]
    readonly_fields = ["slug"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
        models.CharField: {"widget": TextInput(attrs={"size": "153"})},
    }
    inlines = [FactImageInline]

    def get_categories(self, obj):
        if obj.categories.exists():
            return list(obj.categories.values_list("name", flat=True))

    get_categories.short_description = "Categories"


@admin.register(FactCategory)
class FactCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(FactImage)
class FactImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Photographer)
class PhotographerAdmin(admin.ModelAdmin):
    pass
