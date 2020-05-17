from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


class KnowledgeIndexPage(Page):
    intro = RichTextField(blank=True)
    subpage_types = ["KnowledgePage"]
    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]


class KnowledgePage(Page):
    description = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content_panels = Page.content_panels + [
        FieldPanel("description", classname="full"),
        ImageChooserPanel("image"),
    ]
