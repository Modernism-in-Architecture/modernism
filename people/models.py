from django.db import models
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Orderable, Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet


class Person(models.Model):
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
    panels = [
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
        return self.last_name


class Architect(Person):
    pass


class Developer(Person):
    pass


class BuildingOwner(Person):
    pass


class ArchitectsIndexPage(Page):
    parent_page_types = ["people.PersonsIndexPage"]
    subpage_types = ["people.ArchitectPage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["persons"] = ArchitectPage.objects.live().order_by("person__last_name")
        return context

    def get_template(self, request):
        return "people/people_index_page.html"


class ArchitectPage(Page):
    person = models.OneToOneField(Architect, null=True, on_delete=models.SET_NULL)
    parent_page_types = ["people.ArchitectsIndexPage"]
    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel("person"),
    ]

    def get_template(self, request):
        return "people/people_page.html"


class BuildingOwnersIndexPage(Page):
    parent_page_types = ["people.PersonsIndexPage"]
    subpage_types = ["people.BuildingOwnerPage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["persons"] = BuildingOwnerPage.objects.live().order_by(
            "person__last_name"
        )
        return context

    def get_template(self, request):
        return "people/people_index_page.html"


class BuildingOwnerPage(Page):
    person = models.OneToOneField(BuildingOwner, null=True, on_delete=models.SET_NULL)
    parent_page_types = ["people.BuildingOwnersIndexPage"]
    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel("person"),
    ]

    def get_template(self, request):
        return "people/people_page.html"


class DevelopersIndexPage(Page):
    parent_page_types = ["people.PersonsIndexPage"]
    subpage_types = ["people.DeveloperPage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["persons"] = DeveloperPage.objects.live().order_by("person__last_name")
        return context

    def get_template(self, request):
        return "people/people_index_page.html"


class DeveloperPage(Page):
    person = models.OneToOneField(Developer, null=True, on_delete=models.SET_NULL)
    parent_page_types = ["people.DevelopersIndexPage"]
    subpage_types = []
    content_panels = Page.content_panels + [
        FieldPanel("person"),
    ]

    def get_template(self, request):
        return "people/people_page.html"


class PersonsIndexPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = [
        "people.DevelopersIndexPage",
        "people.BuildingOwnersIndexPage",
        "people.ArchitectsIndexPage",
    ]

    def get_template(self, request):
        return "people/people_index_page.html"
