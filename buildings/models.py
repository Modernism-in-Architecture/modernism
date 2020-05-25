from django.core.validators import RegexValidator
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.api import APIField
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.api.fields import ImageRenditionField
from wagtail.images.edit_handlers import ImageChooserPanel

from architects.models import ArchitectPage
from buildings.blocks import GalleryImageBlock
from django_countries.fields import CountryField


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
    country = CountryField(blank_label="(Select Country)", unique=True)

    panels = [
        FieldPanel("country"),
    ]

    def __str__(self):
        return self.country.name

    class Meta:
        verbose_name_plural = "Countries"


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True,
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    panels = [
        FieldPanel("name"),
        FieldPanel("country"),
        ImageChooserPanel("image"),
    ]

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Cities"


class BuildingsIndexPage(Page):
    intro = RichTextField(blank=True)
    subpage_types = ["BuildingPage"]

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    def get_context(self, request):
        context = super().get_context(request)

        buildings = BuildingPage.objects.live()

        tag = request.GET.get("tag")
        if tag:
            buildings = buildings.filter(tags__name=tag)

        context["buildings"] = buildings

        return context


class BuildingPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "buildings.BuildingPage", on_delete=models.CASCADE, related_name="tagged_items"
    )


class BuildingPage(Page):
    name = models.CharField(max_length=250)
    building_type = models.ForeignKey(
        BuildingType, on_delete=models.SET_NULL, null=True, blank=True,
    )
    architect = models.ForeignKey(
        ArchitectPage, on_delete=models.SET_NULL, null=True, blank=True,
    )
    description = RichTextField(blank=True)
    year_of_construction = models.CharField(max_length=4, blank=True)
    directions = RichTextField(blank=True)
    zip_code = models.CharField(max_length=10, default="00000",)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )
    address = models.TextField(blank=True)
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
        FieldPanel("architect"),
        FieldPanel("description", classname="full"),
        FieldPanel("year_of_construction"),
        FieldPanel("directions", classname="full"),
        FieldPanel("zip_code"),
        FieldPanel("city"),
        FieldPanel("country"),
        FieldPanel("address"),
        FieldPanel("lat_long"),
        ImageChooserPanel("feed_image"),
        StreamFieldPanel("gallery_images"),
    ]

    api_fields = [
        APIField("name"),
        APIField("building_type"),
        APIField("architect"),
        APIField("description"),
        APIField("year_of_construction"),
        APIField("city"),
        APIField("country"),
        APIField("address"),
        APIField("lat_long"),
        APIField("tags"),
        APIField("feed_image"),
        APIField(
            "feed_image_thumbnail",
            serializer=ImageRenditionField("fill-400x400", source="feed_image"),
        ),
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
        if self.architect:
            self.tags.add(self.architect.last_name)
        if self.city:
            self.tags.add(self.city.name)
        if self.country:
            self.tags.add(self.country.country.name)
        if self.year_of_construction:
            self.tags.add(self.year_of_construction)

        super(BuildingPage, self).save()
