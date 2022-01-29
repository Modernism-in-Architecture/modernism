from django.contrib.postgres.search import SearchVector
from django.db.models.query import Prefetch
from django.shortcuts import render
from mia_buildings.models import Building, BuildingImage
from mia_facts.models import Source
from rest_framework.decorators import api_view

from .models import Architect, Developer


@api_view(["GET"])
def get_developer_list(
    request, template="mia_people/developer_index.html", extra_context=None
):
    filter_tag = request.GET.get("letter", None)
    search_query = request.GET.get("q", None)

    developer_list = Developer.objects.filter(is_published=True).order_by("last_name")
    alphabet_from_last_names = list(
        dict.fromkeys(
            [x[0] for x in developer_list.values_list("last_name", flat=True)]
        )
    )
    if filter_tag:
        developer_list = developer_list.filter(last_name__startswith=filter_tag)

    if search_query:
        developer_list = developer_list.annotate(
            search=SearchVector(
                "last_name",
                "first_name",
                "description",
            ),
        ).filter(search=search_query)

    context = {
        "persons": developer_list,
        "filter_tag": filter_tag,
        "search_term": search_query,
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
    search_query = request.GET.get("q", None)

    architect_list = Architect.objects.filter(is_published=True).order_by("last_name")
    alphabet_from_last_names = list(
        dict.fromkeys(
            [x[0] for x in architect_list.values_list("last_name", flat=True)]
        )
    )
    if filter_tag:
        architect_list = architect_list.filter(last_name__startswith=filter_tag)

    if search_query:
        architect_list = architect_list.annotate(
            search=SearchVector(
                "last_name",
                "first_name",
                "description",
            ),
        ).filter(search=search_query)

    context = {
        "persons": architect_list,
        "filter_tag": filter_tag,
        "search_term": search_query,
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
        .select_related("death_place__country")
        .prefetch_related("universities")
        .prefetch_related("professor_mentors")
        .prefetch_related("architect_mentors")
        .first()
    )

    if not architect:
        return render(request, "404.html", status=404)

    related_buildings = Building.objects.filter(
        is_published=True, architects__id=architect.id
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
        "source_urls": architect.sources.filter(source_type=Source.SourceType.WEBSITE),
        "source_books": architect.sources.filter(
            source_type__in=[Source.SourceType.BOOK, Source.SourceType.JOURNAL]
        ).prefetch_related("authors"),
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

    if not developer:
        return render(request, "404.html", status=404)

    related_buildings = Building.objects.filter(
        is_published=True, developers__id=developer.id
    ).prefetch_related(
        Prefetch(
            "buildingimage_set",
            queryset=BuildingImage.objects.filter(is_feed_image=True),
            to_attr="feed_images",
        )
    )

    context = {
        "person": developer,
        "related_buildings": related_buildings,
        "source_urls": developer.sources.filter(source_type=Source.SourceType.WEBSITE),
        "source_books": developer.sources.filter(
            source_type__in=[Source.SourceType.BOOK, Source.SourceType.JOURNAL]
        ).prefetch_related("authors"),
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)
