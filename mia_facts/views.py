from django.shortcuts import render
from rest_framework.decorators import api_view


@api_view(["GET"])
def get_fact_list(request, template="mia_facts/index.html", extra_context=None):

    context = {}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)

