from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import FactCategory


class FactCategoryAdmin(ModelAdmin):
    model = FactCategory
    menu_label = "Fact Categories"
    menu_icon = "placeholder"
    menu_order = 293
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("category",)


modeladmin_register(FactCategoryAdmin)
