from django.core.validators import RegexValidator
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.api import APIField
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.edit_handlers import ImageChooserPanel

from buildings.blocks import GalleryImageBlock
from django_countries.fields import CountryField
from people.models import ArchitectPage, BuildingOwnerPage, DeveloperPage


class Tag(TaggitTag):
    class Meta:
        proxy = True


class BuildingType(models.Model):
    name = models.CharField(max_length=255)
    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Building types"


class Country(models.Model):
    country = CountryField(blank_label="(Select a Country)", unique=True)

    panels = [FieldPanel("country")]

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name_plural = "Countries"


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="cities"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("country"),
    ]

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Cities"


class PlacesIndexPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = []


class BuildingsIndexPage(Page):
    subpage_types = ["BuildingPage"]
    parent_page_types = ["home.HomePage"]

    def get_context(self, request):
        context = super().get_context(request)

        buildings = BuildingPage.objects.live()

        tag = request.GET.get("tag")
        if tag:
            buildings = buildings.filter(tags__name=tag)

        context["buildings"] = buildings
        context["countries"] = (
            Country.objects.annotate(number_buildings=models.Count("buildingpage"))
            .filter(number_buildings__gt=0)
            .prefetch_related("cities")
        )
        context["types"] = BuildingType.objects.all()
        context["years"] = (
            BuildingPage.objects.order_by("year_of_construction")
            .distinct("year_of_construction")
            .values_list("year_of_construction", flat=True)
        )
        return context


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
    description = RichTextField(blank=True)
    year_of_construction = models.CharField(max_length=4, blank=True)
    directions = RichTextField(blank=True)
    address = models.TextField(blank=True)
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
    tags = ClusterTaggableManager(through=BuildingPageTag, blank=True)
    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    gallery_images = StreamField([("image", GalleryImageBlock()),], blank=True,)

    content_panels = Page.content_panels + [
        FieldPanel("name"),
        FieldPanel("building_type"),
        InlinePanel("architects", label="Architects"),
        InlinePanel("owners", label="Owners"),
        InlinePanel("developers", label="Developers"),
        FieldPanel("description", classname="full"),
        FieldPanel("year_of_construction"),
        FieldPanel("city"),
        FieldPanel("zip_code"),
        FieldPanel("country"),
        FieldPanel("address"),
        FieldPanel("lat_long"),
        ImageChooserPanel("feed_image"),
        StreamFieldPanel("gallery_images"),
    ]

    api_fields = [
        APIField("name"),
        APIField("city"),
        APIField("country"),
        APIField("address"),
        APIField("lat_long"),
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

    def save(self, *args, **kwargs):
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
