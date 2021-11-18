from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from mia_facts.models import City, Photographer
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


class BuildingImageAdminForm(forms.ModelForm):
    class Meta:
        model = BuildingImage
        fields = "__all__"


@admin.register(BuildingImage)
class BuildingImageAdmin(admin.ModelAdmin):
    # ToDo: Add filter
    form = BuildingImageAdminForm
    autocomplete_fields = ["building"]
    list_display = [
        "building",
        "title",
        "photographer",
        "tag_list",
        "created",
        "updated",
    ]
    readonly_fields = ["tags"]

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

        number_of_building_images = BuildingImage.objects.filter(
            building=obj.building
        ).count()
        if obj.building.city and obj.building.city.country:
            obj.tags.add(obj.building.city.country.name)
        if obj.building.city:
            obj.tags.add(obj.building.city.name)

        obj.title = f"{obj.building.name}-{number_of_building_images + 1}"

        obj.save()


class BuildingImageInline(admin.StackedInline):
    model = BuildingImage
    fields = [
        "image_preview",
        "title",
        "is_published",
        "is_feed_image",
        "description",
        "photographer",
        "tags",
    ]
    readonly_fields = ("image_preview", "tags")
    classes = ["collapse"]

    def has_add_permission(self, request, obj):
        return False


class BuildingAdminForm(forms.ModelForm):
    photographer_choices = list(Photographer.objects.values_list("id", "last_name"))
    photographer_choices.insert(0, (None, "------"))
    photographer = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        choices=photographer_choices,
    )
    multiple_images = forms.ImageField(
        required=False, widget=forms.ClearableFileInput(attrs={"multiple": True})
    )

    class Meta:
        model = Building
        widgets = {
            "subtitle": forms.Textarea(attrs={"rows": "2"}),
            "history": TinyMCE(),
            "description": TinyMCE(),
            "directions": forms.Textarea(attrs={"rows": "3"}),
            "address": forms.Textarea(attrs={"rows": "3"}),
        }
        fields = "__all__"


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    # ToDo: Add filter
    search_fields = ["name", "description"]
    list_display = [
        "name",
        "pk",
        "is_published",
        "year_of_construction",
        "city",
        "created",
        "updated",
        "slug",
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
            None,
            {
                "fields": (
                    "is_published",
                    "name",
                    "slug",
                    "address",
                    "zip_code",
                    "city",
                    "latitude",
                    "longitude",
                    "directions",
                )
            },
        ),
        (
            "GENERAL",
            {
                "classes": ("collapse",),
                "fields": (
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
        (
            "BULK UPLOAD BUILDING IMAGES",
            {
                "description": "Add title, city and country of the building first. So image tags and titles can be generated for all uploaded photos automatically.",
                "classes": ("collapse",),
                "fields": (
                    "photographer",
                    "multiple_images",
                ),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.save()

        if "photographer" or "multiple_images" in form.changed_data:
            photographer_id = form.cleaned_data.get("photographer")
            building_photographer = None
            if photographer_id:
                building_photographer = Photographer.objects.filter(
                    id=photographer_id
                ).first()

            building_photos = request.FILES.getlist("multiple_images")

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

                building_image.title = f"{obj.name}-{index}"

                building_image.save()


@admin.register(ConstructionType)
class ConstructionTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Facade)
class FacadeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Roof)
class RoofAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Window)
class WindowAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(BuildingType)
class BuildingTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(AccessType)
class AccessTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
