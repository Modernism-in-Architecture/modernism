from django.contrib import admin

from .models import (
    Author,
    City,
    Country,
    Fact,
    FactCategory,
    FactImage,
    Photographer,
    Source,
    University,
)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    filter_vertical = ["authors"]


@admin.register(Fact)
class FactAdmin(admin.ModelAdmin):
    filter_vertical = ["categories"]


@admin.register(FactCategory)
class FactCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(FactImage)
class FactImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Photographer)
class PhotographerAdmin(admin.ModelAdmin):
    pass
