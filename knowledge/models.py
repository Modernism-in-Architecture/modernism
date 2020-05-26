from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel


class KnowledgeIndexPage(Page):
    intro = RichTextField(blank=True)
    subpage_types = ["KnowledgePage"]
    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    def get_context(self, request):
        context = super().get_context(request)

        context["facts"] = KnowledgePage.objects.live().order_by("title")

        return context


class KnowledgePageTag(TaggedItemBase):
    content_object = ParentalKey(
        "knowledge.KnowledgePage", on_delete=models.CASCADE, related_name="tagged_items"
    )


class KnowledgePage(Page):
    description = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    tags = ClusterTaggableManager(through=KnowledgePageTag, blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("description", classname="full"),
        ImageChooserPanel("image"),
        FieldPanel("tags"),
    ]

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = "/" + "/".join(
                s.strip("/") for s in [self.get_parent().url, "tags", tag.slug]
            )
        return tags
