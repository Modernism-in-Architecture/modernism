from django.contrib import admin

from .models import Architect, Developer, Professor


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    filter_vertical = ["universities"]


@admin.register(Architect)
class ArchitectAdmin(admin.ModelAdmin):
    filter_vertical = ["universities"]


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    filter_vertical = ["architect_mentors", "professor_mentors", "universities"]
