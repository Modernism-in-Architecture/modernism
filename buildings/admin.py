from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import BuildingType, City, Country, Tag


class BuildingTypeAdmin(ModelAdmin):
    model = BuildingType
    menu_label = "Building Types"
    menu_icon = "placeholder"
    menu_order = 292
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)


class CityAdmin(ModelAdmin):
    model = City
    menu_label = "Cities"
    menu_icon = "placeholder"
    menu_order = 291
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "country")
    ordering = ["name"]


class CountryAdmin(ModelAdmin):
    model = Country
    menu_label = "Countries"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("country",)


class TagAdmin(ModelAdmin):
    model = Tag
    menu_label = "Tags"
    menu_icon = "placeholder"
    menu_order = 294
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "name",
        "slug",
    )


modeladmin_register(BuildingTypeAdmin)
modeladmin_register(CityAdmin)
modeladmin_register(CountryAdmin)
modeladmin_register(TagAdmin)
