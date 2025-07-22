from django.contrib import admin
from mia_buildings.models import BuildingImage

from mia_general.models import ToDoItem


class BuildingImageInline(admin.TabularInline):
    model = BuildingImage
    extra = 0
    fields = ["title", "image", "building", "todo_item"]

@admin.register(ToDoItem)
class ToDoItemAdmin(admin.ModelAdmin):
    list_display = ["title", "city", "is_completed", "created", "updated"]
    list_filter = ["is_completed", "city__country"]
    search_fields = ["title", "city__name", "city__country__name"]
    inlines = [BuildingImageInline]
