import json

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.validators import RegexValidator
from django.db import models
from django.http.request import MultiValueDict, QueryDict
from django.utils.text import slugify
from django_countries import countries
from django_countries.fields import CountryField
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from people.models import ArchitectPage, BuildingOwnerPage, DeveloperPage
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
)
from wagtail.api import APIField
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.edit_handlers import ImageChooserPanel

from buildings.blocks import GalleryImageBlock


class Tag(TaggitTag):
    class Meta:
        proxy = True


class Feature(models.Model):
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    panels = [
        FieldPanel("name"),
    ]


class ConstructionType(Feature):
    pass


class Facade(Feature):
    pass


class Roof(Feature):
    pass


class Window(Feature):
    pass


class Detail(Feature):
    pass


class Position(Feature):
    pass


class BuildingType(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    panels = [FieldPanel("name"), FieldPanel("description", classname="full")]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Building types"


class AccessType(models.Model):
    name = models.CharField(max_length=255)
    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Access types"


class Country(models.Model):
    country = CountryField(blank_label="(Select a Country)", unique=True)
    description = RichTextField(blank=True)
    panels = [FieldPanel("country"), FieldPanel("description", classname="full")]

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name_plural = "Countries"


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="cities"
    )
    description = RichTextField(blank=True)
    panels = [
        FieldPanel("name"),
        FieldPanel("country"),
        FieldPanel("description", classname="full"),
    ]

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Cities"


class PlacesIndexPage(Page):
    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = []

    def clean(self):
        """Override slug."""
        super().clean()
        self.slug = slugify(self.title)


class BuildingsIndexPage(Page):
    subpage_types = ["BuildingPage"]
    parent_page_types = ["home.HomePage"]
    max_count = 1
    ajax_template = "buildings/buildings_list_page.html"
    template = "buildings/buildings_index_page.html"

    def _get_country_code(self, tag_country):
        for code, country in dict(countries).items():
            if tag_country == country:
                return code

    def _get_filtered_buildings(self, cleaned_form_data, buildings):
        architects = cleaned_form_data.get("architects")
        if architects.exists():
            buildings = buildings.filter(
                architects__architect_id__in=architects.values_list("id", flat=True)
            )
            if not buildings:
                return buildings.none()

        developers = cleaned_form_data.get("developers")
        if developers.exists():
            buildings = buildings.filter(
                developers__developer_id__in=developers.values_list("id", flat=True)
            )
            if not buildings:
                return buildings.none()

        countries = cleaned_form_data.get("countries")
        if countries.exists():
            buildings = buildings.filter(
                country_id__in=countries.values_list("id", flat=True)
            )
            if not buildings:
                return buildings.none()

        cities = cleaned_form_data.get("cities")
        if cities.exists():
            buildings = buildings.filter(
                city_id__in=cities.values_list("id", flat=True)
            )
            if not buildings:
                return buildings.none()

        positions = cleaned_form_data.get("positions")
        if positions.exists():
            buildings = buildings.filter(
                positions__id__in=positions.values_list("id", flat=True)
            ).distinct()
            if not buildings:
                return buildings.none()

        details = cleaned_form_data.get("details")
        if details.exists():
            buildings = buildings.filter(
                details__id__in=details.values_list("id", flat=True).distinct()
            )
            if not buildings:
                return buildings.none()

        windows = cleaned_form_data.get("windows")
        if windows.exists():
            buildings = buildings.filter(
                windows__id__in=windows.values_list("id", flat=True).distinct()
            )
        roofs = cleaned_form_data.get("roofs")
        if roofs.exists():
            buildings = buildings.filter(
                roofs__id__in=roofs.values_list("id", flat=True).distinct()
            )
            if not buildings:
                return buildings.none()

        facades = cleaned_form_data.get("facades")
        if facades.exists():
            buildings = buildings.filter(
                facades__id__in=facades.values_list("id", flat=True).distinct()
            )
            if not buildings:
                return buildings.none()

        construction_types = cleaned_form_data.get("construction_types")
        if construction_types.exists():
            buildings = buildings.filter(
                construction_types__id__in=construction_types.values_list(
                    "id", flat=True
                ).distinct()
            )
            if not buildings:
                return buildings.none()

        years = cleaned_form_data.get("years")
        if years:
            buildings = buildings.filter(year_of_construction__in=years)
            if not buildings:
                return buildings.none()

        building_type = cleaned_form_data.get("building_types")
        if building_type:
            buildings = buildings.filter(building_type=building_type)
            if not buildings:
                return buildings.none()

        access_type = cleaned_form_data.get("access_type")
        if access_type:
            buildings = buildings.filter(access_type=access_type)
            if not buildings:
                return buildings.none()

        is_protected_monument = cleaned_form_data.get("protected_monument")
        if is_protected_monument != "":
            buildings = buildings.filter(protected_monument=is_protected_monument)
            if not buildings:
                return buildings.none()

        storey = cleaned_form_data.get("storey")
        if storey != "":
            buildings = buildings.filter(storey=storey)
            if not buildings:
                return buildings.none()

        return buildings.distinct()

    def get_context(self, request):
        context = super().get_context(request)

        from buildings.forms import BuildingsFilterForm

        all_buildings = BuildingPage.objects.live().order_by("-first_published_at")

        if request.method == "POST":
            building_form = BuildingsFilterForm(request.POST)
            request.session["filter-request"] = dict(request.POST)

            if building_form.is_valid():
                context["form"] = building_form
                all_buildings = self._get_filtered_buildings(
                    building_form.cleaned_data, all_buildings
                )

        else:
            current_filter_settings = request.session.get("filter-request")
            context["form"] = BuildingsFilterForm()

            if current_filter_settings is not None:
                for setting, value in list(current_filter_settings.items()):
                    try:
                        if value[0] == "":
                            del current_filter_settings[setting]
                    except KeyError:
                        continue

                filter_query_dict = QueryDict("", mutable=True)
                filter_query_dict.update(MultiValueDict(current_filter_settings))
                building_form = BuildingsFilterForm(filter_query_dict)

                if building_form.is_valid():
                    context["form"] = building_form
                    all_buildings = self._get_filtered_buildings(
                        building_form.cleaned_data, all_buildings
                    )

        context["buildings"] = all_buildings
        return context

    def clean(self):
        """Override slug."""
        super().clean()
        self.slug = slugify(self.title)


class BuildingPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "buildings.BuildingPage", on_delete=models.CASCADE, related_name="tagged_items"
    )


class BuildingPageArchitectRelation(models.Model):
    page = ParentalKey(
        "buildings.BuildingPage", on_delete=models.CASCADE, related_name="architects"
    )
    architect = ParentalKey(
        "people.ArchitectPage", on_delete=models.CASCADE, related_name="buildings"
    )
    panels = [
        FieldPanel("architect"),
    ]

    class Meta:
        unique_together = ("page", "architect")


class BuildingPageOwnerRelation(models.Model):
    page = ParentalKey(
        "buildings.BuildingPage", on_delete=models.CASCADE, related_name="owners"
    )
    owner = ParentalKey(
        "people.BuildingOwnerPage", on_delete=models.CASCADE, related_name="buildings"
    )
    panels = [
        FieldPanel("owner"),
    ]

    class Meta:
        unique_together = ("page", "owner")


class BuildingPageDeveloperRelation(models.Model):
    page = ParentalKey(
        "buildings.BuildingPage", on_delete=models.CASCADE, related_name="developers"
    )
    developer = ParentalKey(
        "people.DeveloperPage", on_delete=models.CASCADE, related_name="buildings"
    )
    panels = [
        FieldPanel("developer"),
    ]

    class Meta:
        unique_together = ("page", "developer")


class BuildingPage(Page):
    name = models.CharField(max_length=250, unique=True)
    building_type = models.ForeignKey(
        BuildingType, on_delete=models.SET_NULL, null=True, blank=True,
    )
    access_type = models.ForeignKey(
        AccessType, on_delete=models.SET_NULL, null=True, blank=True,
    )
    protected_monument = models.BooleanField(default=False)
    storey = models.IntegerField(null=True, blank=True)
    positions = ParentalManyToManyField("buildings.Position", blank=True)
    details = ParentalManyToManyField("buildings.Detail", blank=True)
    windows = ParentalManyToManyField("buildings.Window", blank=True)
    roofs = ParentalManyToManyField("buildings.Roof", blank=True)
    facades = ParentalManyToManyField("buildings.Facade", blank=True)
    construction_types = ParentalManyToManyField(
        "buildings.ConstructionType", blank=True
    )
    todays_use = models.CharField(max_length=300, blank=True)
    description = RichTextField(blank=True)
    year_of_construction = models.CharField(max_length=4, blank=True)
    directions = models.TextField(
        blank=True,
        help_text="Note here how to get there, public transport information or alike.",
    )
    address = models.TextField(
        blank=True, help_text="Please, provide a street name and/or number."
    )
    zip_code = models.CharField(max_length=10, default="00000",)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )
    lat_long = models.CharField(
        max_length=36,
        help_text="Comma separated lat/long. (Ex. 64.144367, -21.939182) \
                   Right click Google Maps and select 'What's Here'",
        validators=[
            RegexValidator(
                regex=r"^(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)$",
                message="Lat Long must be a comma-separated numeric lat and long",
                code="invalid_lat_long",
            ),
        ],
    )
    # latitude = models.DecimalField(max_digits=23, decimal_places=20)
    # longitude = models.DecimalField(max_digits=23, decimal_places=20)
    tags = ClusterTaggableManager(through=BuildingPageTag, blank=True)
    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="This image will be used to preview the building on the buildings overview page.",
    )
    gallery_images = StreamField([("image", GalleryImageBlock()),], blank=True,)

    prefetch_related = [
        "tags",
        "construction_types",
        "facades",
        "roofs",
        "windows",
        "details",
        "positions",
        "gallery_images",
    ]
    select_related = [
        "feed_image",
        "country",
        "city",
        "access_type",
        "building_type",
    ]

    content_panels = [
        FieldPanel("name"),
        MultiFieldPanel(
            [
                FieldRowPanel([FieldPanel("zip_code"), FieldPanel("country"),]),
                FieldRowPanel([FieldPanel("city"), FieldPanel("address"),]),
                FieldRowPanel([FieldPanel("lat_long"),]),
                FieldRowPanel([FieldPanel("directions"),]),
            ],
            heading="Address",
        ),
        MultiFieldPanel(
            [
                FieldPanel("building_type"),
                FieldPanel("protected_monument"),
                FieldRowPanel(
                    [FieldPanel("storey"), FieldPanel("year_of_construction"),]
                ),
                FieldRowPanel([FieldPanel("access_type"), FieldPanel("todays_use"),]),
                FieldPanel("construction_types", widget=forms.CheckboxSelectMultiple),
                FieldRowPanel(
                    [
                        FieldPanel("windows", widget=forms.CheckboxSelectMultiple),
                        FieldPanel("roofs", widget=forms.CheckboxSelectMultiple,),
                        FieldPanel("facades", widget=forms.CheckboxSelectMultiple),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel("positions", widget=forms.CheckboxSelectMultiple),
                        FieldPanel("details", widget=forms.CheckboxSelectMultiple),
                    ]
                ),
            ],
            heading="Features",
        ),
        FieldPanel("description", classname="full"),
        MultiFieldPanel(
            [
                InlinePanel("architects", label="Architects"),
                InlinePanel("developers", label="Developers"),
            ],
            heading="People",
        ),
        ImageChooserPanel("feed_image"),
        StreamFieldPanel("gallery_images"),
    ]

    api_fields = [
        APIField("name"),
        APIField("city"),
        APIField("country"),
        APIField("address"),
        APIField("lat_long"),
        APIField("gallery_images"),
    ]

    parent_page_types = ["buildings.BuildingsIndexPage"]
    subpage_types = []

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = "/" + "/".join(
                s.strip("/") for s in [self.get_parent().url, "tags", tag.slug]
            )
        return tags

    @property
    def teaser_tags(self):
        types = BuildingType.objects.all().values_list("name", flat=True)
        tags = self.tags.exclude(name__in=types)
        for tag in tags:
            tag.url = "/" + "/".join(
                s.strip("/") for s in [self.get_parent().url, "tags", tag.slug]
            )
        return tags

    def clean(self):
        """Override title and slug."""
        super().clean()
        self.title = self.name
        self.slug = slugify(self.title)

    def save(self, *args, **kwargs):
        """Add tags from new values."""
        self.tags.clear()
        if self.building_type:
            self.tags.add(self.building_type.name)
        if self.city:
            self.tags.add(self.city.name)
        if self.country:
            self.tags.add(self.country.country.name)
        if self.year_of_construction:
            self.tags.add(self.year_of_construction)

        super(BuildingPage, self).save()
