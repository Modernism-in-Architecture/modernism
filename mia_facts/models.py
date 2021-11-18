from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Countries"


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        "mia_facts.Country", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Cities"


class University(models.Model):
    name = models.CharField(max_length=250, unique=True)
    city = models.ForeignKey(
        "mia_facts.City", on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Universities"


class Author(models.Model):
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250)

    def __str__(self):
        return self.last_name


class Photographer(models.Model):
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250)
    contact_info = models.CharField(max_length=250, blank=True)
    url = models.URLField(max_length=250, blank=True)

    def __str__(self):
        name = self.last_name
        if self.first_name:
            name = f"{self.first_name} {self.last_name}"
        return name


class Source(models.Model):
    class SourceType(models.TextChoices):
        WEBSITE = "WE", "Website"
        BOOK = "BK", "Book"
        JOURNAL = "JL", "Journal"

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    source_type = models.CharField(
        max_length=2,
        choices=SourceType.choices,
        default=SourceType.WEBSITE,
    )
    authors = models.ManyToManyField("mia_facts.Author", blank=True)
    title = models.CharField(max_length=250)
    year = models.CharField(max_length=4, blank=True)
    place_of_publication = models.CharField(max_length=250, blank=True)
    publisher = models.CharField(max_length=250, blank=True)
    isbn = models.CharField(max_length=250, blank=True)
    edition = models.PositiveIntegerField(null=True, blank=True)
    url = models.URLField(max_length=250, blank=True)

    def __str__(self):
        return self.title


class FactCategory(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class FactImage(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    image = models.ImageField(upload_to="mia-facts", null=True, blank=True)
    fact = models.ForeignKey(
        "mia_facts.Fact", on_delete=models.SET_NULL, null=True, blank=True
    )
    title = models.CharField(max_length=250, blank=True)
    photographer = models.ForeignKey(
        "mia_facts.Photographer", on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title if self.title else self.pk}"


class Fact(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField("mia_facts.FactCategory", blank=True)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(max_length=254, blank=True)
    sources = models.ManyToManyField("mia_facts.Source", blank=True)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.title))
        return super().save(*args, **kwargs)
