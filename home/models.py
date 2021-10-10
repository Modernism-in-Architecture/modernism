from base.mixins import CustomMetadataPageMixin
from django.db import models
from django.utils.text import slugify
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page


class HomePage(CustomMetadataPageMixin, Page):
    max_count = 1
    hero_text = models.CharField(max_length=400, blank=True)
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("hero_text", classname="full"),
        FieldPanel("body", classname="full"),
    ]

    def clean(self):
        """Override slug."""
        super().clean()
        self.slug = slugify(self.title)


class GeneralPage(CustomMetadataPageMixin, Page):
    body = RichTextField(blank=True)
    subpage_types = []
    parent_page_types = ["home.HomePage"]
    content_panels = Page.content_panels + [
        FieldPanel("body", classname="full"),
    ]

    def clean(self):
        """Override slug."""
        super().clean()
        self.slug = slugify(self.title)
