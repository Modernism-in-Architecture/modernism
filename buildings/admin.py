from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import BuildingType, City, Country


class BuildingTypeAdmin(ModelAdmin):
    model = BuildingType
    menu_label = "Building Type"
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name",)


class CityAdmin(ModelAdmin):
    model = City
    menu_label = "City"
    menu_icon = "placeholder"
    menu_order = 291
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "name",
        "zip_code",
    )


class CountryAdmin(ModelAdmin):
    model = Country
    menu_label = "Country"
    menu_icon = "placeholder"
    menu_order = 292
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("country",)


modeladmin_register(BuildingTypeAdmin)
modeladmin_register(CityAdmin)
modeladmin_register(CountryAdmin)
