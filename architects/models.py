from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


class ArchitectsIndexPage(Page):
    intro = RichTextField(blank=True)

    parent_page_types = ["home.HomePage"]
    subpage_types = ["architects.ArchitectPage"]

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    def get_context(self, request):
        context = super().get_context(request)

        context["architects"] = ArchitectPage.objects.live().order_by("last_name")

        return context


class ArchitectPage(Page):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    birthday = models.DateField("Birthday", blank=True, null=True)
    place_of_birth = models.CharField(max_length=100, blank=True)
    place_of_death = models.CharField(max_length=100, blank=True)
    day_of_death = models.DateField("Day of Death", blank=True, null=True)
    description = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    parent_page_types = ["architects.ArchitectsIndexPage"]
    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("birthday"),
        FieldPanel("place_of_birth"),
        FieldPanel("day_of_death"),
        FieldPanel("place_of_death"),
        FieldPanel("description", classname="full"),
        ImageChooserPanel("image"),
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
