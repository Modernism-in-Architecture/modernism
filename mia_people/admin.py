from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Architect, Developer, Professor


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "is_published", "created", "pk", "slug"]
    filter_horizontal = ["universities"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


@admin.register(Architect)
class ArchitectAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "is_published", "created", "pk", "slug"]
    filter_horizontal = ["architect_mentors", "professor_mentors", "universities"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "is_published", "created", "pk", "slug"]
    filter_horizontal = [
        "architect_mentors",
        "professor_mentors",
        "universities",
    ]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
