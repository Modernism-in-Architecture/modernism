from django.contrib.postgres.search import SearchVector
from django.shortcuts import render
from rest_framework.decorators import api_view

from mia_facts.models import Fact, FactCategory, Source


@api_view(["GET"])
def get_fact_list(request, template="mia_facts/fact_index.html", extra_context=None):
    filter_tag = request.GET.get("tag", None)
    search_query = request.GET.get("q", None)

    if filter_tag:
        facts = (
            Fact.objects.filter(
                is_published=True, categories__name__startswith=filter_tag
            )
            .prefetch_related("categories")
            .prefetch_related("factimage_set")
        )
    else:
        facts = (
            Fact.objects.filter(is_published=True)
            .prefetch_related("categories")
            .prefetch_related("factimage_set")
        )

    if search_query:
        facts = facts.annotate(
            search=SearchVector(
                "title",
                "description",
            ),
        ).filter(search=search_query)

    categories = FactCategory.objects.filter(fact__isnull=False).distinct()

    context = {
        "facts": facts,
        "categories": categories,
        "filter_tag": filter_tag,
        "search_term": search_query,
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


@api_view(["GET"])
def get_fact_details(
    request,
    slug,
    template="mia_facts/fact_details.html",
    extra_context=None,
):
    fact = (
        Fact.objects.filter(is_published=True, slug=slug)
        .prefetch_related("categories")
        .prefetch_related("sources")
        .first()
    )

    if not fact:
        return render(request, "404.html", status=404)

    context = {
        "fact": fact,
        "source_urls": fact.sources.filter(source_type=Source.SourceType.WEBSITE),
        "source_books": fact.sources.filter(
            source_type__in=[Source.SourceType.BOOK, Source.SourceType.JOURNAL]
        ).prefetch_related("authors"),
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)
