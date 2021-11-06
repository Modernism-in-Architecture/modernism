from django.shortcuts import render
from rest_framework.decorators import api_view

from .models import Fact, FactCategory


@api_view(["GET"])
def get_fact_list(request, template="mia_facts/fact_index.html", extra_context=None):
    filter_tag = request.GET.get("tag", None)
    if filter_tag:
        facts = Fact.objects.filter(
            is_published=True, categories__name__startswith=filter_tag
        ).prefetch_related("categories")
    else:
        facts = Fact.objects.filter(is_published=True).prefetch_related("categories")

    categories = FactCategory.objects.filter(fact__isnull=False).distinct()
    context = {"facts": facts, "categories": categories, "filter_tag": filter_tag}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


@api_view(["GET"])
def get_fact_details(
    request, slug, template="mia_facts/fact_details.html", extra_context=None,
):

    fact = (
        Fact.objects.filter(is_published=True, slug=slug)
        .prefetch_related("categories")
        .prefetch_related("sources")
        .first()
    )

    context = {"fact": fact}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)
