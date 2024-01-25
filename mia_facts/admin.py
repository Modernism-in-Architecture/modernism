from django.contrib import admin
from django.db import models
from django.forms.widgets import TextInput
from tinymce.widgets import TinyMCE

from modernism.tools import validate_and_clean_content_markup
from .admin_forms import FactAdminForm
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
    list_display = [
        "name",
        "country",
        "get_number_of_related_buildings",
        "get_number_of_related_people",
        "get_number_of_related_universities",
    ]
    search_fields = ["name"]
    ordering = ["name"]

    def get_number_of_related_buildings(self, obj):
        return obj.building_set.count()

    get_number_of_related_buildings.short_description = "Number of related buildings"

    def get_number_of_related_people(self, obj):
        return obj.birth_place_people.count() + obj.death_place_people.count()

    get_number_of_related_people.short_description = "Number of related people"

    def get_number_of_related_universities(self, obj):
        return obj.university_set.count()

    get_number_of_related_universities.short_description = (
        "Number of related universities"
    )

    def get_queryset(self, request):
        qs = super(CityAdmin, self).get_queryset(request)
        return (
            qs.select_related("country")
            .prefetch_related("building_set")
            .prefetch_related("birth_place_people")
            .prefetch_related("death_place_people")
        )


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
    form = FactAdminForm
    search_fields = ["title", "description"]
    list_display = [
        "title",
        "pk",
        "is_published",
        "description_is_clean",
        "get_categories",
        "created",
    ]
    list_filter = ["categories"]
    filter_horizontal = ["categories", "sources"]
    readonly_fields = ["slug"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
        models.CharField: {"widget": TextInput(attrs={"size": "153"})},
    }
    inlines = [FactImageInline]

    @admin.display(description="Categories")
    def get_categories(self, obj):
        if obj.categories.exists():
            return list(obj.categories.values_list("name", flat=True))

    @admin.display(description="Description clean")
    def description_is_clean(self, building):
        was_clean, _ = validate_and_clean_content_markup(building.description)
        return was_clean

    description_is_clean.boolean = True


@admin.register(FactCategory)
class FactCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(FactImage)
class FactImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Photographer)
class PhotographerAdmin(admin.ModelAdmin):
    pass
