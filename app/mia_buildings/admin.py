import ast
from gettext import ngettext

from adminsortable2.admin import SortableAdminBase, SortableTabularInline
from django import forms
from django.contrib import admin, messages
from django.db import models
from django.forms import Textarea, TextInput
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import path
from mia_facts.models import Photographer
from mia_general.models import ToDoItem
from modernism.tools import validate_and_clean_content_markup

from mia_buildings import admin_views
from mia_buildings.admin_filters import (
    CityListFilter,
    CountryListFilter,
    ImageBuildingEmptyFilter,
)

from .admin_forms import (
    AssignOrCreateToDoItemForm,
    BuildingAdminForm,
    BuildingForImageSelectionAdminForm,
)
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


class BuildingImageAdminForm(forms.ModelForm):
    class Meta:
        model = BuildingImage
        fields = "__all__"


@admin.register(BuildingImage)
class BuildingImageAdmin(admin.ModelAdmin):
    form = BuildingImageAdminForm
    search_fields = [
        "title",
        "building__name",
        "building__city__name",
        "building__city__country__name",
    ]
    autocomplete_fields = ["building", "photographer"]
    actions = ["add_images_to_building", "assign_or_create_todoitem", "archive_image"]
    list_display = [
        "title",
        "image_preview",
        "id",
        "is_published",
        "is_feed_image",
        "is_archived",
        "building",
        "todo_item",
        "photographer",
        "thumbnails_created",
        "created",
        "updated",
    ]
    list_filter = ["is_published", "is_archived", ImageBuildingEmptyFilter]
    readonly_fields = ["tags", "image_preview", "thumbnails_created"]
    fields = [
        "image_preview",
        "title",
        "is_published",
        "is_feed_image",
        "is_archived",
        "thumbnails_created",
        "image",
        "building",
        "description",
        "photographer",
        "tags",
    ]
    change_list_template = "admin/buildingimage_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_admin_urls = [
            path(
                "bulkupload-images/",
                admin_views.bulkupload_images,
                name="bulkupload-images",
            ),
        ]
        return custom_admin_urls + urls

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("building")
            .select_related("photographer")
            .prefetch_related("tags")
        )

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())

    def save_model(self, request, obj, form, change):
        obj.save()

        if obj.building and obj.building.city and obj.building.city.country:
            obj.tags.add(obj.building.city.country.name)

        if obj.building and obj.building.city:
            obj.tags.add(obj.building.city.name)

        obj.save()

    @admin.action(description="Add images to a building gallery")
    def add_images_to_building(self, request, queryset):
        if "apply" in request.POST:
            form = BuildingForImageSelectionAdminForm(request.POST)
            if form.is_valid():
                building = form.cleaned_data["building"]
                selected_images = ast.literal_eval(form.cleaned_data["_images"])
                building_images = BuildingImage.objects.filter(id__in=selected_images)
                building.buildingimage_set.add(*building_images)
                self.message_user(
                    request,
                    f"{building} successfully received {len(selected_images)} gallery images.",
                )
            return HttpResponseRedirect(request.get_full_path())
        else:
            form = BuildingForImageSelectionAdminForm()

        return render(
            request,
            "admin/add_images_to_building.html",
            {
                "images": queryset,
                "form": form,
                "title": "Add images to a building gallery",
            },
        )

    @admin.action(description="Archive selected images")
    def archive_image(self, request, queryset):
        updated = queryset.update(is_archived=True)
        self.message_user(
            request,
            ngettext("%d image archived.", "%d images archived.", updated) % updated,
            messages.SUCCESS,
        )
        return None

    @admin.action(description="Assign images to ToDoItem")
    def assign_or_create_todoitem(self, request, queryset):
        if "apply" in request.POST:
            form = AssignOrCreateToDoItemForm(request.POST)

            if form.is_valid():
                selected_images = ast.literal_eval(form.cleaned_data["_images"])
                queryset = BuildingImage.objects.filter(pk__in=selected_images)
                todo = form.cleaned_data["todo_item"]

                if not todo:
                    todo = ToDoItem.objects.create(
                        title=form.cleaned_data["working_title"],
                        city=form.cleaned_data["city"],
                        notes=form.cleaned_data.get("notes", ""),
                    )

                queryset.update(todo_item=todo)

                self.message_user(
                    request,
                    f"{queryset.count()} images assigned to ToDoItem '{todo.title}'.",
                )
                return redirect(request.get_full_path())
        else:
            form = AssignOrCreateToDoItemForm(
                initial={"_selected_action": [image.pk for image in queryset]}
            )

        return render(
            request,
            "admin/assign_or_create_todoitem.html",
            {"form": form, "images": queryset, "title": "Assign images to ToDoItem"},
        )


class BuildingImageInline(SortableTabularInline):
    model = BuildingImage
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("image_preview", "image_order", "image"),
                    (
                        "is_published",
                        "is_feed_image",
                    ),
                    ("title", "description", "photographer"),
                )
            },
        ),
    )
    readonly_fields = ("image_preview", "tags")
    autocomplete_fields = ["photographer"]
    classes = ["collapse"]
    extra = 0

    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "auto"})},
        models.TextField: {"widget": Textarea(attrs={"width": "auto"})},
    }


@admin.register(Building)
class BuildingAdmin(SortableAdminBase, admin.ModelAdmin):
    change_list_template = "admin/building_changelist.html"
    change_form_template = "admin/building_change_form.html"
    search_fields = [
        "name",
        "name_addition",
        "description",
        "city__name",
        "city__country__name",
    ]
    list_display = [
        "name",
        "name_addition",
        "pk",
        "is_published",
        "slug",
        "city",
        "year_of_construction",
        "created",
        "updated",
        "history_is_clean",
        "description_is_clean",
        "seo_title",
    ]
    list_filter = [
        CityListFilter,
        CountryListFilter,
        "is_published",
    ]
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
    readonly_fields = [
        "slug",
    ]
    autocomplete_fields = ["city"]
    form = BuildingAdminForm
    inlines = [BuildingImageInline]

    fieldsets = (
        (
            "GENERAL",
            {
                "fields": (
                    "is_published",
                    "name",
                    "name_addition",
                    "slug",
                    "seo_title",
                    "address",
                    "zip_code",
                    "city",
                    "latitude",
                    "longitude",
                    "directions",
                    "protected_monument",
                    "year_of_construction",
                    "todays_use",
                    "access_type",
                    "storey",
                ),
            },
        ),
        (
            "DESCRIPTION",
            {
                "classes": ("collapse",),
                "fields": ("subtitle", "history", "description", "sources"),
            },
        ),
        (
            "PEOPLE",
            {
                "classes": ("collapse",),
                "fields": (
                    "architects",
                    "developers",
                ),
            },
        ),
        (
            "FEATURES",
            {
                "classes": ("collapse",),
                "fields": (
                    "windows",
                    "roofs",
                    "positions",
                    "facades",
                    "details",
                    "construction_types",
                    "building_types",
                ),
            },
        ),
    )

    @admin.display(description="History clean")
    def history_is_clean(self, building):
        was_clean, _ = validate_and_clean_content_markup(building.history)
        return was_clean

    history_is_clean.boolean = True

    @admin.display(description="Description clean")
    def description_is_clean(self, building):
        was_clean, _ = validate_and_clean_content_markup(building.description)
        return was_clean

    description_is_clean.boolean = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("city__country")

    def save_model(self, request, obj, form, change):
        obj.save()

        if (
            "photographer" in form.changed_data
            or "multiple_images" in form.changed_data
        ):
            photographer_id = form.cleaned_data.get("photographer")
            building_photographer = None
            if photographer_id:
                building_photographer = Photographer.objects.filter(
                    id=photographer_id
                ).first()

            building_photos = request.FILES.getlist("multiple_images")
            number_of_existing_images = obj.buildingimage_set.count()

            for index, photo in enumerate(building_photos):
                building_image, created = BuildingImage.objects.get_or_create(
                    building=obj, image=photo
                )
                if building_photographer:
                    building_image.photographer = building_photographer
                if obj.city and obj.city.country:
                    building_image.tags.add(obj.city.country.name)
                if obj.city:
                    building_image.tags.add(obj.city.name)

                building_image.title = f"{obj.name}-{number_of_existing_images + index}"

                building_image.save()


@admin.register(ConstructionType)
class ConstructionTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]
    list_display = ["name", "number_of_related_buildings", "id"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("building_set")

    @admin.display(description="Number of Buildings")
    def number_of_related_buildings(self, construction_type):
        return construction_type.building_set.count()


@admin.register(Facade)
class FacadeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]
    list_display = ["name", "number_of_related_buildings", "id"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("building_set")

    @admin.display(description="Number of Buildings")
    def number_of_related_buildings(self, facade):
        return facade.building_set.count()


@admin.register(Roof)
class RoofAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]
    list_display = ["name", "number_of_related_buildings", "id"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("building_set")

    @admin.display(description="Number of Buildings")
    def number_of_related_buildings(self, roof):
        return roof.building_set.count()


@admin.register(Window)
class WindowAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]
    list_display = ["name", "number_of_related_buildings", "id"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("building_set")

    @admin.display(description="Number of Buildings")
    def number_of_related_buildings(self, window):
        return window.building_set.count()


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]
    list_display = ["name", "number_of_related_buildings", "id"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("building_set")

    @admin.display(description="Number of Buildings")
    def number_of_related_buildings(self, detail):
        return detail.building_set.count()


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]
    list_display = ["name", "number_of_related_buildings", "id"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("building_set")

    @admin.display(description="Number of Buildings")
    def number_of_related_buildings(self, position):
        return position.building_set.count()


@admin.register(BuildingType)
class BuildingTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]
    list_display = ["name", "number_of_related_buildings", "id"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("building_set")

    @admin.display(description="Number of Buildings")
    def number_of_related_buildings(self, building_type):
        return building_type.building_set.count()


@admin.register(AccessType)
class AccessTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    ordering = ["name"]
    list_display = ["name", "number_of_related_buildings", "id"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("building_set")

    @admin.display(description="Number of Buildings")
    def number_of_related_buildings(self, access_type):
        return access_type.building_set.count()
