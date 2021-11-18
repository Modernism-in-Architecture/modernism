from django.db.models.query import Prefetch
from django.shortcuts import render
from mia_buildings.models import Building, BuildingImage
from rest_framework.decorators import api_view

from .models import Architect, Developer


@api_view(["GET"])
def get_developer_list(
    request, template="mia_people/developer_index.html", extra_context=None
):
    filter_tag = request.GET.get("letter", None)
    developer_list = Developer.objects.filter(is_published=True).order_by("last_name")
    alphabet_from_last_names = list(
        dict.fromkeys(
            [x[0] for x in developer_list.values_list("last_name", flat=True)]
        )
    )
    if filter_tag:
        developer_list = developer_list.filter(last_name__startswith=filter_tag)
    context = {
        "persons": developer_list,
        "filter_tag": filter_tag,
        "last_name_alphabet": alphabet_from_last_names,
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


@api_view(["GET"])
def get_architect_list(
    request, template="mia_people/architect_index.html", extra_context=None
):
    filter_tag = request.GET.get("letter", None)
    architect_list = Architect.objects.filter(is_published=True).order_by("last_name")
    alphabet_from_last_names = list(
        dict.fromkeys(
            [x[0] for x in architect_list.values_list("last_name", flat=True)]
        )
    )
    if filter_tag:
        architect_list = architect_list.filter(last_name__startswith=filter_tag)
    context = {
        "persons": architect_list,
        "filter_tag": filter_tag,
        "last_name_alphabet": alphabet_from_last_names,
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


@api_view(["GET"])
def get_architect_details(
    request,
    slug,
    template="mia_people/architect_details.html",
    extra_context=None,
):

    architect = (
        Architect.objects.filter(slug=slug)
        .select_related("birth_place__country")
        .prefetch_related("universities")
        .prefetch_related("professor_mentors")
        .prefetch_related("architect_mentors")
        .first()
    )

    related_buildings = Building.objects.filter(
        architects__id=architect.id
    ).prefetch_related(
        Prefetch(
            "buildingimage_set",
            queryset=BuildingImage.objects.filter(is_feed_image=True),
            to_attr="feed_images",
        )
    )
    context = {
        "person": architect,
        "related_buildings": related_buildings,
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


@api_view(["GET"])
def get_developer_details(
    request,
    slug,
    template="mia_people/developer_details.html",
    extra_context=None,
):

    developer = (
        Developer.objects.filter(is_published=True, slug=slug)
        .select_related("birth_place__country")
        .prefetch_related("universities")
        .first()
    )

    context = {"person": developer}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)
