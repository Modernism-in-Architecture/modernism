from buildings.models import City, Country
from django import forms
from django.db import models
from django.utils.text import slugify
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.search.backends import get_search_backend


class FactsIndexPage(Page):
    max_count = 1
    intro = RichTextField(blank=True)
    parent_page_types = ["home.HomePage"]
    subpage_types = ["facts.FactPage"]
    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    def get_context(self, request):
        context = super().get_context(request)
        search_query = request.GET.get("q", None)

        facts = FactPage.objects.live().order_by("title")

        if search_query:
            facts = facts.search(search_query)
        tag = request.GET.get("tag")
        if tag:
            facts = facts.filter(tags__name=tag)

        context["facts"] = facts
        context["categories"] = FactCategory.objects.order_by("category")
        context["search_term"] = search_query
        return context

    def clean(self):
        """Override slug."""
        super().clean()
        self.slug = slugify(self.title)


class FactPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "facts.FactPage", on_delete=models.CASCADE, related_name="tagged_items"
    )


class FactCategory(models.Model):
    category = models.CharField(max_length=250, unique=True)
    panels = [
        FieldPanel("category"),
    ]

    def __str__(self):
        return self.category

    class Meta:
        verbose_name_plural = "Categories"


class ArchitectUniversity(models.Model):
    name = models.CharField(max_length=250, unique=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = RichTextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Architect Universities"


class FactPage(Page):
    description = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    categories = ParentalManyToManyField(
        "facts.FactCategory", blank=True, related_name="fact"
    )
    tags = ClusterTaggableManager(through=FactPageTag, blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("description", classname="full"),
        FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
        ImageChooserPanel("image"),
    ]
    parent_page_types = ["facts.FactsIndexPage"]
    subpage_types = []
    search_fields = Page.search_fields + [
        index.SearchField("title"),
        index.SearchField("description"),
    ]

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = "/" + "/".join(
                s.strip("/") for s in [self.get_parent().url, "tags", tag.slug]
            )
        return tags

    def clean(self):
        """Override slug."""
        super().clean()
        self.slug = slugify(self.title)

    def save(self, *args, **kwargs):
        """Add tags from new values."""
        self.tags.clear()
        self.tags.add(*self.categories.all().values_list("category", flat=True))

        super(FactPage, self).save()
