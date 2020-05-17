from django.core.validators import RegexValidator
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel

from architects.models import ArchitectPage


class BuildingType(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel("name"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Building types"


class BuildingsIndexPage(Page):
    intro = RichTextField(blank=True)
    subpage_types = ["BuildingPage"]

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    def get_context(self, request):
        context = super().get_context(request)

        context["buildings"] = BuildingPage.objects.child_of(self).live()
        return context


class BuildingPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "buildings.BuildingPage", on_delete=models.CASCADE, related_name="tagged_items"
    )


class BuildingPage(Page):
    # TODO: Add InformationSource, Catalog Number
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
    gallery_images = StreamField([("image", ImageChooserBlock()),], blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("name"),
        FieldPanel("building_type"),
        FieldPanel("architect"),
        FieldPanel("description", classname="full"),
        FieldPanel("year_of_construction"),
        FieldPanel("directions", classname="full"),
        FieldPanel("address"),
        FieldPanel("lat_long"),
        ImageChooserPanel("feed_image"),
        StreamFieldPanel("gallery_images"),
        FieldPanel("tags"),
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
