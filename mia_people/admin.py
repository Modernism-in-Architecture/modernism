from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Architect, Developer, Professor


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    filter_horizontal = ["universities"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


@admin.register(Architect)
class ArchitectAdmin(admin.ModelAdmin):
    filter_horizontal = ["universities"]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    filter_horizontal = [
        "architect_mentors",
        "professor_mentors",
        "universities",
    ]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE()},
    }
