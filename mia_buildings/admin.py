import ast

from adminsortable.admin import NonSortableParentAdmin, SortableStackedInline
from django import forms
from django.contrib import admin
from django.db import models
from django.forms import Textarea, TextInput
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from mia_facts.models import Photographer
from tinymce.widgets import TinyMCE

from mia_buildings import views
from mia_buildings.forms import (
    BuildingForImageSelectionAdminForm,
    MultipleImageFileField,
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
        "tags__name",
    ]
    list_filter = [
        ("building__city__country", admin.RelatedOnlyFieldListFilter),
        ("building__city", admin.RelatedOnlyFieldListFilter),
    ]
    autocomplete_fields = ["building"]
    actions = ["add_images_to_building"]
    list_display = [
        "title",
        "image_preview",
        "is_published",
        "is_feed_image",
        "building",
        "tag_list",
        "photographer",
        "id",
        "created",
        "updated",
    ]
    readonly_fields = [
        "tags",
        "image_preview",
    ]
    fields = [
        "image_preview",
        "title",
        "is_published",
        "is_feed_image",
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
                views.bulkupload_images,
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

    add_images_to_building.short_description = "Add images to a building gallery"


class BuildingImageInline(SortableStackedInline):
    model = BuildingImage
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("image_preview", "title", "image"),
                    ("is_published", "is_feed_image", "description", "photographer"),
                )
            },
        ),
    )
    readonly_fields = ("image_preview", "tags")
    classes = ["collapse"]
    extra = 0

    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "50"})},
        models.TextField: {"widget": Textarea(attrs={"rows": 1, "cols": 20})},
    }


class BuildingAdminForm(forms.ModelForm):
    multiple_images = MultipleImageFileField(required=False)
    photographer = forms.ChoiceField(
        required=False,
        widget=forms.Select,
    )

    class Meta:
        model = Building
        widgets = {
            "subtitle": forms.Textarea(attrs={"rows": "2"}),
            "seo_title": forms.Textarea(attrs={"rows": "2"}),
            "history": TinyMCE(
                mce_attrs={"convert_urls": False, "browser_spellcheck": True}
            ),
            "description": TinyMCE(
                mce_attrs={"convert_urls": False, "browser_spellcheck": True}
            ),
            "directions": forms.Textarea(attrs={"rows": "3"}),
            "address": forms.Textarea(attrs={"rows": "3"}),
        }
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_photographer_choices()

    def set_photographer_choices(self):
        photographers = Photographer.objects.values_list("id", "last_name").order_by(
            "last_name"
        )
        choices = [("", "------")] + list(photographers)
        self.fields["photographer"].choices = choices


@admin.register(Building)
class BuildingAdmin(NonSortableParentAdmin):
    search_fields = ["name", "description", "city__name", "city__country__name"]
    list_display = [
        "name",
        "pk",
        "is_published",
        "published_on_twitter",
        "year_of_construction",
        "city",
        "created",
        "updated",
        "slug",
        "seo_title",
    ]
    list_filter = [
        "is_published",
        ("city__country", admin.RelatedOnlyFieldListFilter),
        ("city", admin.RelatedOnlyFieldListFilter),
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
        "published_on_twitter",
    ]
    autocomplete_fields = ["city"]
    form = BuildingAdminForm
    inlines = [BuildingImageInline]

    change_form_template = "admin/building_change_form.html"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_published",
                    "published_on_twitter",
                    "name",
                    "slug",
                    "seo_title",
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

    def get_queryset(self, request):
        qs = super(BuildingAdmin, self).get_queryset(request)
        return qs.select_related("city__country")

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
