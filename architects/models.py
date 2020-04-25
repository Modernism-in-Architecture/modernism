from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


class ArchitectsIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]


class ArchitectPage(Page):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    birthday = models.DateField("Birthday", blank=True, null=True)
    day_of_death = models.DateField("Day of Death", blank=True, null=True)
    description = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content_panels = Page.content_panels + [
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("birthday"),
        FieldPanel("day_of_death"),
        FieldPanel("description", classname="full"),
        ImageChooserPanel("image"),
    ]
