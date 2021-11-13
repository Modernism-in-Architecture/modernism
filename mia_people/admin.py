from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Architect, Developer, Professor


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    raw_id_fields = ["birth_place"]
    search_fields = ["last_name", "first_name", "description"]
    list_display = ["last_name", "first_name", "is_published", "created", "pk", "slug"]
    filter_horizontal = ["universities", "sources"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
    ordering = ("last_name",)


@admin.register(Architect)
class ArchitectAdmin(admin.ModelAdmin):
    raw_id_fields = ["birth_place"]
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


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    raw_id_fields = ["birth_place"]
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
