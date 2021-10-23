from django.contrib import admin

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


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    raw_id_fields = ["country", "city"]
    filter_vertical = [
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


@admin.register(BuildingImage)
class BuildingImageAdmin(admin.ModelAdmin):
    pass


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
