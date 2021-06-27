from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from buildings.models import (
    AccessType,
    ArchitectPage,
    BuildingPage,
    BuildingType,
    City,
    ConstructionType,
    Country,
    Detail,
    DeveloperPage,
    Facade,
    Position,
    Roof,
    Window,
)


class EmptyChoiceField(forms.ChoiceField):
    def __init__(
        self,
        choices=(),
        empty_label=None,
        required=True,
        widget=None,
        label=None,
        initial=None,
        help_text=None,
        *args,
        **kwargs
    ):

        # prepend an empty label if it exists (and field is not required!)
        if not required and empty_label is not None:
            choices = tuple([(u"", empty_label)] + list(choices))

        super(EmptyChoiceField, self).__init__(
            choices=choices,
            required=required,
            widget=widget,
            label=label,
            initial=initial,
            help_text=help_text,
            *args,
            **kwargs
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
    protected_monument = EmptyChoiceField(
        required=False,
        empty_label="----",
        choices=[(True, "yes"), (False, "no")],
        widget=forms.Select(attrs={"class": "feature-select"}),
    )

    storeys = BuildingPage.objects.filter(storey__isnull=False).values_list(
        "storey", flat=True
    )
    storey = EmptyChoiceField(
        required=False,
        empty_label="----",
        choices=[(storey, storey) for storey in set(storeys)],
        widget=forms.Select(attrs={"class": "feature-select"}),
    )
    architects = forms.ModelMultipleChoiceField(
        queryset=ArchitectPage.objects.filter(buildings__isnull=False).distinct(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    developers = forms.ModelMultipleChoiceField(
        queryset=DeveloperPage.objects.filter(buildings__isnull=False).distinct(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
    years_choices = (
        BuildingPage.objects.exclude(year_of_construction__exact="")
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
