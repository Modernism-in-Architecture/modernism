from wagtail.contrib.modeladmin.helpers import WagtailBackendSearchHandler
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from facts.models import ArchitectUniversity, FactCategory, FactPage


class FactCategoryAdmin(ModelAdmin):
    model = FactCategory
    menu_label = "Fact Categories"
    menu_icon = "form"
    menu_order = 205
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("category",)


class ArchitectUniversityAdmin(ModelAdmin):
    model = ArchitectUniversity
    menu_label = "Architect Universities"
    menu_icon = "form"
    menu_order = 206
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = (
        "name",
        "city",
        "country",
    )


class FactAdmin(ModelAdmin):
    model = FactPage
    list_display = (
        "title",
        "fact_categories",
    )
    menu_icon = "arrow-right"
    menu_order = 204
    search_handler_class = WagtailBackendSearchHandler

    def fact_categories(self, obj):
        categories = obj.categories.values_list("category", flat=True)
        return ", ".join([category for category in categories])


modeladmin_register(FactCategoryAdmin)
modeladmin_register(FactAdmin)
modeladmin_register(ArchitectUniversityAdmin)
