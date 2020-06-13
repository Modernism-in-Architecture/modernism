from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Architect, BuildingOwner, Developer


class ArchitectAdmin(ModelAdmin):
    model = Architect
    menu_label = "Architects"
    menu_icon = "placeholder"
    menu_order = 287
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("last_name",)


class BuildingOwnerAdmin(ModelAdmin):
    model = BuildingOwner
    menu_label = "Owners"
    menu_icon = "placeholder"
    menu_order = 288
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("last_name",)


class DeveloperAdmin(ModelAdmin):
    model = Developer
    menu_label = "Developers"
    menu_icon = "placeholder"
    menu_order = 289
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("last_name",)


modeladmin_register(ArchitectAdmin)
modeladmin_register(DeveloperAdmin)
modeladmin_register(BuildingOwnerAdmin)
