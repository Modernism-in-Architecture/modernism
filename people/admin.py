from wagtail.contrib.modeladmin.helpers import WagtailBackendSearchHandler
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from people.models import ArchitectPage, DeveloperPage, ProfessorPage


class ArchitectAdmin(ModelAdmin):
    model = ArchitectPage
    list_display = (
        "last_name",
        "first_name",
        "birthday",
        "place_of_birth",
        "day_of_death",
    )
    menu_icon = "arrow-right"
    menu_order = 202
    search_handler_class = WagtailBackendSearchHandler


class DeveloperAdmin(ModelAdmin):
    model = DeveloperPage
    list_display = (
        "last_name",
        "first_name",
        "birthday",
        "place_of_birth",
        "day_of_death",
    )
    menu_icon = "arrow-right"
    menu_order = 203
    search_handler_class = WagtailBackendSearchHandler


class ProfessorAdmin(ModelAdmin):
    model = ProfessorPage
    list_display = (
        "last_name",
        "first_name",
        "birthday",
        "place_of_birth",
        "day_of_death",
    )
    menu_icon = "arrow-right"
    menu_order = 202
    search_handler_class = WagtailBackendSearchHandler


modeladmin_register(ArchitectAdmin)
modeladmin_register(DeveloperAdmin)
modeladmin_register(ProfessorAdmin)
