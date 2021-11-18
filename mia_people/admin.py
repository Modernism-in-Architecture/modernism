from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Architect, Developer, Professor


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    autocomplete_fields = ["birth_place", "death_place"]
    search_fields = ["last_name", "first_name", "description"]
    list_display = ["last_name", "first_name", "is_published", "created", "pk", "slug"]
    filter_horizontal = ["universities", "sources"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    ordering = ("last_name",)
    readonly_fields = [
        "slug",
    ]


@admin.register(Architect)
class ArchitectAdmin(admin.ModelAdmin):
    autocomplete_fields = ["birth_place", "death_place"]
    search_fields = ["last_name", "first_name", "description"]
    list_display = ["last_name", "first_name", "is_published", "created", "pk", "slug"]
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
    ]


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    autocomplete_fields = ["birth_place", "death_place"]
    search_fields = ["last_name", "first_name", "description"]
    list_display = ["last_name", "first_name", "is_published", "created", "pk", "slug"]
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
