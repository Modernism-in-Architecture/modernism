from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import widgets
from tinymce.widgets import TinyMCE

from .models import (
    AccessType,
    Building,
    BuildingImage,
    BuildingType,
    ConstructionType,
    Detail,
    Facade,
    Position,
    Roof,
    Window,
)


class BuildingAdminForm(forms.ModelForm):
    class Meta:
        model = Building
        widgets = {"description": TinyMCE()}
        fields = "__all__"


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    raw_id_fields = ["country", "city"]
    filter_horizontal = [
        "windows",
        "roofs",
        "positions",
        "facades",
        "details",
        "construction_types",
        "building_types",
        "developers",
        "architects",
        "sources",
    ]
    form = BuildingAdminForm


class BuildingImageAdminForm(forms.ModelForm):
    class Meta:
        model = BuildingImage
        widgets = {"tags": FilteredSelectMultiple("tags", is_stacked=False)}
        fields = "__all__"


@admin.register(BuildingImage)
class BuildingImageAdmin(admin.ModelAdmin):
    form = BuildingImageAdminForm


@admin.register(ConstructionType)
class ConstructionTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Facade)
class FacadeAdmin(admin.ModelAdmin):
    pass


@admin.register(Roof)
class RoofAdmin(admin.ModelAdmin):
    pass


@admin.register(Window)
class WindowAdmin(admin.ModelAdmin):
    pass


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(BuildingType)
class BuildingTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(AccessType)
class AccessTypeAdmin(admin.ModelAdmin):
    pass
