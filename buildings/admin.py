from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import BuildingType


class BuildingTypeAdmin(ModelAdmin):
    model = BuildingType
    menu_label = "Building Type"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)


modeladmin_register(BuildingTypeAdmin)
