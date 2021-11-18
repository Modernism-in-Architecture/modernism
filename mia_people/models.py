from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


class Person(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    is_published = models.BooleanField(default=False)
    slug = models.SlugField(max_length=254, blank=True)

    last_name = models.CharField(
        max_length=250,
        help_text="You can add a company name here too if appropriate.",
    )
    first_name = models.CharField(max_length=250, blank=True)
    birthday = models.DateField(
        blank=True,
        null=True,
        help_text="If you only know the year, just set a random value for month and day, but tick the following box.",
    )
    birth_year_known_only = models.BooleanField(
        default=False, help_text="Tick the box if you only know the year."
    )
    birth_place = models.ForeignKey(
        "mia_facts.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="birth_place_people",
    )
    day_of_death = models.DateField(
        blank=True,
        null=True,
        help_text="If you only know the year, just set a random value for month and day, but tick the following box.",
    )
    death_year_known_only = models.BooleanField(
        default=False, help_text="Tick the box if you only know the year."
    )
    death_place = models.ForeignKey(
        "mia_facts.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="death_place_people",
    )
    universities = models.ManyToManyField(
        "mia_facts.University", blank=True, related_name="universities"
    )
    description = models.TextField(blank=True)

    sources = models.ManyToManyField("mia_facts.Source", blank=True)

    def __str__(self):
        name = self.last_name
        if self.first_name:
            name = f"{self.first_name} {self.last_name}"
        return name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["first_name", "last_name"], name="fullname")
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            first_name = unidecode(self.first_name)
            last_name = unidecode(self.last_name)
            self.slug = slugify(first_name + " " + last_name)
        return super().save(*args, **kwargs)


class Professor(Person):
    architect_mentors = models.ManyToManyField("mia_people.Architect", blank=True)
    professor_mentors = models.ManyToManyField("self", blank=True)
    is_active_architect = models.BooleanField(
        default=False, help_text="Is/Was the professor active as modernist architect?"
    )
    is_active_developer = models.BooleanField(
        default=False, help_text="Is/Was the professor active as developer?"
    )


class Developer(Person):
    pass


class Architect(Person):
    is_developer = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)
    professor_mentors = models.ManyToManyField("mia_people.Professor", blank=True)
    architect_mentors = models.ManyToManyField("self", blank=True)
