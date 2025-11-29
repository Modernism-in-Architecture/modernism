from django.contrib.admin import SimpleListFilter
from mia_facts.models import City, Country


class CityListFilter(SimpleListFilter):
    title = "City"
    template = "admin/custom_city_filter.html"
    parameter_name = "city_id"

    def lookups(self, request, model_admin):
        return (
            City.objects.filter(building__isnull=False)
            .values_list("id", "name")
            .distinct()
            .order_by("name")
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(city=self.value())


class CountryListFilter(SimpleListFilter):
    title = "Country"
    template = "admin/custom_country_filter.html"
    parameter_name = "country_id"

    def lookups(self, request, model_admin):
        return (
            Country.objects.filter(city__building__isnull=False)
            .values_list("id", "name")
            .distinct()
            .order_by("name")
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(city__country=self.value())


class ImageBuildingEmptyFilter(SimpleListFilter):
    title = "Building"
    parameter_name = "building__isnull"
    empty_label = "Has no building"
    not_empty_label = "Has building"

    def lookups(self, request, model_admin):
        # 1 = isnull=True, 0 = isnull=False
        return (("1", self.empty_label), ("0", self.not_empty_label))

    def queryset(self, request, queryset):
        value = self.value()
        if value == "1":
            return queryset.filter(building__isnull=True)
        if value == "0":
            return queryset.filter(building__isnull=False)
        return queryset
