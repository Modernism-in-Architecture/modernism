from django.db import models
from django.utils.text import slugify
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page, PageManager
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


class PeoplePageManager(PageManager):
    def get_queryset(self):
        return super().get_queryset().order_by("last_name", "first_name")


class PersonPage(Page):
    is_creatable = False
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
    objects = PeoplePageManager()

    content_panels = [
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

    def clean(self):
        """Override title and slug."""
        super().clean()
        new_title = f"{self.first_name} {self.last_name}"
        self.title = new_title
        self.slug = slugify(new_title)

    def get_template(self, request):
        return "people/people_page.html"


class PersonsIndexPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = [
        "people.DevelopersIndexPage",
        "people.BuildingOwnersIndexPage",
        "people.ArchitectsIndexPage",
    ]
    max_count = 1

    def get_template(self, request):
        return "people/people_index_page.html"


class ArchitectsIndexPage(Page):
    parent_page_types = ["people.PersonsIndexPage"]
    subpage_types = ["people.ArchitectPage"]
    max_count = 1

    def get_context(self, request):
        context = super().get_context(request)
        context["persons"] = ArchitectPage.objects.live().order_by("last_name")
        return context

    def get_template(self, request):
        return "people/people_index_page.html"


class BuildingOwnersIndexPage(Page):
    parent_page_types = ["people.PersonsIndexPage"]
    subpage_types = ["people.BuildingOwnerPage"]
    max_count = 1

    def get_context(self, request):
        context = super().get_context(request)
        context["persons"] = BuildingOwnerPage.objects.live().order_by("last_name")
        return context

    def get_template(self, request):
        return "people/people_index_page.html"


class DevelopersIndexPage(Page):
    parent_page_types = ["people.PersonsIndexPage"]
    subpage_types = ["people.DeveloperPage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["persons"] = DeveloperPage.objects.live().order_by("last_name")
        return context

    def get_template(self, request):
        return "people/people_index_page.html"


class ArchitectPage(PersonPage):
    parent_page_types = ["people.ArchitectsIndexPage"]
    subpage_types = []


class BuildingOwnerPage(PersonPage):
    parent_page_types = ["people.BuildingOwnersIndexPage"]
    subpage_types = []


class DeveloperPage(PersonPage):
    parent_page_types = ["people.DevelopersIndexPage"]
    subpage_types = []
