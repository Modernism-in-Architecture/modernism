from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.html import mark_safe
from mia_facts.models import Photographer
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
        widgets = {"tags": FilteredSelectMultiple("tags", is_stacked=False)}
        fields = "__all__"


@admin.register(BuildingImage)
class BuildingImageAdmin(admin.ModelAdmin):
    # ToDo: Add search and filter
    form = BuildingImageAdminForm
    list_display = [
        "building",
        "title",
        "photographer",
        "tag_list",
        "created",
        "updated",
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())


class BuildingImageInline(admin.StackedInline):
    model = BuildingImage
    extra = 0
    classes = ["collapse"]
    readonly_fields = ("image_preview",)


class BuildingAdminForm(forms.ModelForm):
    photographer_choices = list(Photographer.objects.values_list("id", "last_name"))
    photographer_choices.insert(0, (None, "------"))
    photographer = forms.ChoiceField(
        required=False, widget=forms.Select, choices=photographer_choices,
    )
    multiple_images = forms.ImageField(
        required=False, widget=forms.ClearableFileInput(attrs={"multiple": True})
    )

    class Meta:
        model = Building
        widgets = {
            "history": TinyMCE(),
            "description": TinyMCE(),
            "directions": forms.Textarea(attrs={"rows": "3"}),
            "address": forms.Textarea(attrs={"rows": "3"}),
        }
        fields = "__all__"


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    # ToDo: Add search and filter
    list_display = [
        "name",
        "pk",
        "is_published",
        "year_of_construction",
        "city",
        "country",
        "created",
        "updated",
    ]
    raw_id_fields = ["country", "city"]
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
    form = BuildingAdminForm
    inlines = [BuildingImageInline]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_published",
                    "name",
                    "address",
                    "zip_code",
                    "city",
                    "country",
                    ("latitude", "longitude"),
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
            {"classes": ("collapse",), "fields": ("architects", "developers",),},
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
                "fields": ("photographer", "multiple_images",),
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
                image_tags = building_image.tags.all()

                if building_photographer:
                    building_image.photographer = building_photographer
                if obj.country and obj.country not in image_tags:
                    building_image.tags.add(obj.country.country.name)
                if obj.city and obj.city not in image_tags:
                    building_image.tags.add(obj.city.name)

                building_image.title = f"{obj.name}-{index}"

                building_image.save()


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
