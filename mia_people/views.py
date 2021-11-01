from django.shortcuts import render
from rest_framework.decorators import api_view


@api_view(["GET"])
def get_developer_list(
    request, template="mia_people/developer_list.html", extra_context=None
):

    context = {}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


@api_view(["GET"])
def get_architect_list(
    request, template="mia_people/architect_list.html", extra_context=None
):

    context = {}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)

