from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from django.utils.text import slugify
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, PageManager
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class PeoplePageManager(PageManager):
    def get_queryset(self):
        return super().get_queryset().order_by("last_name", "first_name")


class PersonPage(Page):
    is_creatable = False
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(
        max_length=250, help_text="You can add a company name here too if appropriate."
    )
    birthday = models.DateField(
        "Birthday",
        blank=True,
        null=True,
        help_text="If you only know the year, just set a random value for month and day, but tick the following box.",
    )
    birth_year_known_only = models.BooleanField(
        default=False, help_text="Tick the box if you only know the birth year."
    )
    place_of_birth = models.CharField(
        max_length=100,
        blank=True,
        help_text="Add in following format: city, country. E.g. 'Leipzig, Germany'",
    )
    place_of_death = models.CharField(
        max_length=100,
        blank=True,
        help_text="Add in following format: city, country. E.g. 'Leipzig, Germany'",
    )
    day_of_death = models.DateField(
        "Day of Death",
        blank=True,
        null=True,
        help_text="If you only know the year, just set a random value for month and day, but tick the following box.",
    )
    death_year_known_only = models.BooleanField(
        default=False, help_text="Tick the box if you only know the birth year."
    )
    universities = ParentalManyToManyField(
        "facts.ArchitectUniversity", blank=True, related_name="universities"
    )
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
        MultiFieldPanel(
            [FieldRowPanel([FieldPanel("last_name"), FieldPanel("first_name")])],
            heading="Name",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("birthday", classname="col6"),
                        FieldPanel("birth_year_known_only", classname="col6"),
                    ]
                ),
                FieldPanel("place_of_birth"),
            ],
            heading="Birthday",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("day_of_death", classname="col6"),
                        FieldPanel("death_year_known_only", classname="col6"),
                    ]
                ),
                FieldPanel("place_of_death"),
            ],
            heading="Death",
        ),
        FieldPanel(
            "universities",
            widget=FilteredSelectMultiple(
                verbose_name="universities", is_stacked=False,
            ),
        ),
        FieldPanel("description", classname="full"),
        ImageChooserPanel("image"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("last_name"),
        index.SearchField("first_name"),
        index.SearchField("description"),
    ]

    def __str__(self):
        name = self.last_name
        if self.first_name:
            name = f"{self.first_name} {self.last_name}"
        return name

    def clean(self):
        """Override title and slug."""
        super().clean()
        new_title = self.last_name
        if self.first_name:
            new_title = f"{self.first_name} {self.last_name}"
        self.title = new_title
        self.slug = slugify(new_title)

    def get_template(self, request):
        return "people/people_page.html"


class PersonsIndexPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = [
        "people.DevelopersIndexPage",
        "people.ProfessorIndexPage",
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
        architects = ArchitectPage.objects.live().order_by("last_name")

        search_query = request.GET.get("q", None)
        if search_query:
            architects = architects.search(search_query)

        context["persons"] = architects
        context["search_term"] = search_query
        return context

    def get_template(self, request):
        return "people/people_index_page.html"


class DevelopersIndexPage(Page):
    parent_page_types = ["people.PersonsIndexPage"]
    subpage_types = ["people.DeveloperPage"]
    max_count = 1

    def get_context(self, request):
        context = super().get_context(request)
        developers = DeveloperPage.objects.live().order_by("last_name")

        search_query = request.GET.get("q", None)
        if search_query:
            developers = developers

        context["persons"] = developers.search(search_query)
        context["search_term"] = search_query
        return context

    def get_template(self, request):
        return "people/people_index_page.html"


class ProfessorIndexPage(Page):
    parent_page_types = ["people.PersonsIndexPage"]
    subpage_types = ["people.ProfessorPage"]
    max_count = 1


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


class ProfessorPage(PersonPage):
    parent_page_types = ["people.ProfessorIndexPage"]
    subpage_types = []

    architect_mentors = ParentalManyToManyField(
        "people.ArchitectPage", blank=True, related_name="professors"
    )
    professor_mentors = ParentalManyToManyField(
        "self", blank=True, related_name="mentors"
    )
    is_active_architect = models.BooleanField(
        default=False, help_text="Is/Was the professor active as modernist architect?"
    )
    is_active_developer = models.BooleanField(
        default=False, help_text="Is/Was the professor active as developer?"
    )
    content_panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("last_name", classname="col6"),
                        FieldPanel("first_name", classname="col6"),
                    ]
                )
            ],
            heading="Name",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("is_active_architect", classname="col6"),
                        FieldPanel("is_active_developer", classname="col6"),
                    ]
                )
            ],
            heading="Activity",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("birthday", classname="col6"),
                        FieldPanel("birth_year_known_only", classname="col6"),
                    ]
                ),
                FieldPanel("place_of_birth"),
            ],
            heading="Birthday",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("day_of_death", classname="col6"),
                        FieldPanel("death_year_known_only", classname="col6"),
                    ]
                ),
                FieldPanel("place_of_death"),
            ],
            heading="Death",
        ),
        MultiFieldPanel(
            [
                FieldPanel(
                    "professor_mentors",
                    widget=FilteredSelectMultiple(
                        verbose_name="Professors", is_stacked=False,
                    ),
                ),
                FieldPanel(
                    "architect_mentors",
                    widget=FilteredSelectMultiple(
                        verbose_name="Architects", is_stacked=False,
                    ),
                ),
            ],
            heading="Mentors",
        ),
        FieldPanel(
            "universities",
            widget=FilteredSelectMultiple(
                verbose_name="universities", is_stacked=False,
            ),
        ),
        FieldPanel("description", classname="full"),
        ImageChooserPanel("image"),
    ]


class DeveloperPage(PersonPage):
    parent_page_types = ["people.DevelopersIndexPage"]
    subpage_types = []


class ArchitectPage(PersonPage):
    parent_page_types = ["people.ArchitectsIndexPage"]
    subpage_types = []

    professor_mentors = ParentalManyToManyField("people.ProfessorPage", blank=True)
    architect_mentors = ParentalManyToManyField("self", blank=True)

    content_panels = [
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("last_name", classname="col6"),
                        FieldPanel("first_name", classname="col6"),
                    ]
                )
            ],
            heading="Name",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("birthday", classname="col6"),
                        FieldPanel("birth_year_known_only", classname="col6"),
                    ]
                ),
                FieldPanel("place_of_birth"),
            ],
            heading="Birthday",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("day_of_death", classname="col6"),
                        FieldPanel("death_year_known_only", classname="col6"),
                    ]
                ),
                FieldPanel("place_of_death"),
            ],
            heading="Death",
        ),
        MultiFieldPanel(
            [
                FieldPanel(
                    "professor_mentors",
                    widget=FilteredSelectMultiple(
                        verbose_name="Professors", is_stacked=False,
                    ),
                ),
                FieldPanel(
                    "architect_mentors",
                    widget=FilteredSelectMultiple(
                        verbose_name="Architects", is_stacked=False,
                    ),
                ),
            ],
            heading="Mentors",
        ),
        FieldPanel(
            "universities",
            widget=FilteredSelectMultiple(
                verbose_name="universities", is_stacked=False,
            ),
        ),
        FieldPanel("description", classname="full"),
        ImageChooserPanel("image"),
    ]


class BuildingOwnerPage(PersonPage):
    parent_page_types = ["people.BuildingOwnersIndexPage"]
    subpage_types = []
