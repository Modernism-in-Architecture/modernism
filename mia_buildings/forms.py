from django import forms
from mia_facts.models import City, Country
from mia_people.models import Architect, Developer

from mia_buildings.models import (
    AccessType,
    Building,
    BuildingType,
    ConstructionType,
    Detail,
    Facade,
    Position,
    Roof,
    Window,
)


class BuildingsFilterForm(forms.Form):
    building_types = forms.ModelChoiceField(
        queryset=BuildingType.objects.all().order_by("name"),
        widget=forms.Select(attrs={"class": "feature-select"}),
        required=False,
    )
    access_types = forms.ModelChoiceField(
        queryset=AccessType.objects.all().order_by("name"),
        widget=forms.Select(attrs={"class": "feature-select"}),
        required=False,
    )
    protected_monument = forms.ChoiceField(
        required=False,
        choices=[("", "---------"), (True, "yes"), (False, "no")],
        widget=forms.Select(attrs={"class": "feature-select"}),
    )
    storeys = Building.objects.filter(storey__isnull=False).values_list(
        "storey", flat=True
    )
    storey = forms.ChoiceField(
        required=False,
        choices=[("", "---------")] + [(storey, storey) for storey in set(storeys)],
        widget=forms.Select(attrs={"class": "feature-select"}),
    )
    architects = forms.ModelMultipleChoiceField(
        queryset=Architect.objects.filter(building__isnull=False).distinct(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    developers = forms.ModelMultipleChoiceField(
        queryset=Developer.objects.filter(building__isnull=False).distinct(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    years_choices = (
        Building.objects.exclude(year_of_construction__exact="")
        .distinct("year_of_construction")
        .order_by("year_of_construction")
        .values_list("year_of_construction", flat=True)
    )
    years = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        choices=[(year, year) for year in years_choices],
    )

    countries = forms.ModelMultipleChoiceField(
        queryset=Country.objects.all().order_by("country"),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    cities = forms.ModelMultipleChoiceField(
        queryset=City.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    positions = forms.ModelMultipleChoiceField(
        queryset=Position.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    details = forms.ModelMultipleChoiceField(
        queryset=Detail.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    windows = forms.ModelMultipleChoiceField(
        queryset=Window.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    roofs = forms.ModelMultipleChoiceField(
        queryset=Roof.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    facades = forms.ModelMultipleChoiceField(
        queryset=Facade.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    construction_types = forms.ModelMultipleChoiceField(
        queryset=ConstructionType.objects.all().order_by("name"),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
