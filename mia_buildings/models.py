from unidecode import unidecode

from easy_thumbnails.templatetags.thumbnail import thumbnail_url
from taggit.managers import TaggableManager

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import slugify


class Feature(models.Model):
    name = models.CharField(max_length=254, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ConstructionType(Feature):
    pass


class Facade(Feature):
    pass


class Roof(Feature):
    pass


class Window(Feature):
    pass


class Detail(Feature):
    pass


class Position(Feature):
    pass


class BuildingType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Building types"


class AccessType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Access types"


class BuildingImage(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    image = models.ImageField(upload_to="original_images", null=True, blank=True)
    building = models.ForeignKey(
        "mia_buildings.Building", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_published = models.BooleanField(default=True)
    is_feed_image = models.BooleanField(default=False)
    title = models.CharField(max_length=250, blank=True)
    photographer = models.ForeignKey(
        "mia_facts.Photographer", on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField(blank=True)
    tags = TaggableManager(blank=True)
    image_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ["image_order"]

    def __str__(self):
        return f"{self.title}"

    def image_preview(self):
        if self.image:
            thumbnail = thumbnail_url(self.image, "preview")
            return mark_safe(f"<img src={thumbnail} />")
        else:
            return "(No image)"


class Building(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=254, unique=True)
    name_addition = models.CharField(
        max_length=254,
        blank=True,
        help_text="Add here the original name or info displayed in brackets behind the title. Do not add the brackets.",
    )
    subtitle = models.CharField(max_length=254, blank=True)
    todays_use = models.CharField(max_length=254, blank=True)
    year_of_construction = models.CharField(max_length=4, blank=True)
    history = models.TextField(blank=True)
    description = models.TextField(blank=True)

    directions = models.TextField(blank=True)
    address = models.TextField(blank=True)
    zip_code = models.CharField(max_length=16, blank=True)
    city = models.ForeignKey(
        "mia_facts.City", on_delete=models.SET_NULL, null=True, blank=True
    )
    latitude = models.DecimalField(
        max_digits=23, decimal_places=20, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=23, decimal_places=20, null=True, blank=True
    )

    protected_monument = models.BooleanField(default=False)
    storey = models.IntegerField(null=True, blank=True)
    access_type = models.ForeignKey(
        AccessType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    building_types = models.ManyToManyField("mia_buildings.BuildingType", blank=True)
    positions = models.ManyToManyField("mia_buildings.Position", blank=True)
    details = models.ManyToManyField("mia_buildings.Detail", blank=True)
    windows = models.ManyToManyField("mia_buildings.Window", blank=True)
    roofs = models.ManyToManyField("mia_buildings.Roof", blank=True)
    facades = models.ManyToManyField("mia_buildings.Facade", blank=True)
    construction_types = models.ManyToManyField(
        "mia_buildings.ConstructionType", blank=True
    )

    architects = models.ManyToManyField("mia_people.Architect", blank=True)
    developers = models.ManyToManyField("mia_people.Developer", blank=True)

    sources = models.ManyToManyField("mia_facts.Source", blank=True)

    is_published = models.BooleanField(default=False)
    slug = models.SlugField(max_length=254, blank=True)

    seo_title = models.CharField(max_length=61, blank=True)

    published_on_twitter = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)
