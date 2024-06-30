from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from modernism.tools import validate_and_clean_content_markup
from .admin_forms import ArchitectAdminForm, DeveloperAdminForm, ProfessorAdminForm
from .models import Architect, Developer, Professor


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    form = DeveloperAdminForm
    autocomplete_fields = ["birth_place", "death_place"]
    search_fields = ["last_name", "first_name", "description"]
    list_display = [
        "last_name",
        "first_name",
        "is_published",
        "description_is_clean",
        "birth_place",
        "death_place",
        "created",
        "pk",
        "slug",
    ]
    filter_horizontal = ["universities", "sources"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    ordering = ("last_name",)
    readonly_fields = [
        "slug",
    ]

    @admin.display(description="Description clean")
    def description_is_clean(self, building):
        was_clean, _ = validate_and_clean_content_markup(building.description)
        return was_clean

    description_is_clean.boolean = True


@admin.register(Architect)
class ArchitectAdmin(admin.ModelAdmin):
    form = ArchitectAdminForm
    autocomplete_fields = ["birth_place", "death_place"]
    search_fields = ["last_name", "first_name", "description"]
    list_display = [
        "last_name",
        "first_name",
        "is_published",
        "description_is_clean",
        "birth_place",
        "death_place",
        "created",
        "pk",
        "slug",
    ]
    filter_horizontal = [
        "architect_mentors",
        "professor_mentors",
        "universities",
        "sources",
    ]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    ordering = ("last_name",)
    readonly_fields = [
        "slug",
    ]
    fields = [
        "is_published",
        "is_developer",
        "is_professor",
        "last_name",
        "first_name",
        "birthday",
        "birth_year_known_only",
        "birth_place",
        "day_of_death",
        "death_year_known_only",
        "death_place",
        "universities",
        "architect_mentors",
        "professor_mentors",
        "description",
        "sources",
        "seo_title",
    ]

    @admin.display(description="Description clean")
    def description_is_clean(self, building):
        was_clean, _ = validate_and_clean_content_markup(building.description)
        return was_clean

    description_is_clean.boolean = True


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    form = ProfessorAdminForm
    autocomplete_fields = ["birth_place", "death_place"]
    search_fields = ["last_name", "first_name", "description"]
    list_display = [
        "last_name",
        "first_name",
        "is_published",
        "description_is_clean",
        "birth_place",
        "death_place",
        "created",
        "pk",
        "slug",
    ]
    filter_horizontal = [
        "architect_mentors",
        "professor_mentors",
        "universities",
        "sources",
    ]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    ordering = ("last_name",)
    readonly_fields = [
        "slug",
    ]

    @admin.display(description="Description clean")
    def description_is_clean(self, building):
        was_clean, _ = validate_and_clean_content_markup(building.description)
        return was_clean

    description_is_clean.boolean = True
